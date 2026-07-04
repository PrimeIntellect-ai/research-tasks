# test_final_state.py
import os
import json
import csv

def get_expected_anomalies(csv_path):
    anomalies = []
    prev_ts = None
    prev_loc = None

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            ts = int(row['timestamp'])
            loc = row['locale']
            strings = int(row['strings_translated'])
            errors = int(row['errors_reported'])

            # Skip consecutive duplicates
            if ts == prev_ts and loc == prev_loc:
                continue

            prev_ts = ts
            prev_loc = loc

            if strings > 100:
                rate = errors / strings
                if rate > 0.20:
                    anomalies.append({
                        "timestamp": ts,
                        "locale": loc,
                        "error_rate": round(rate, 2)
                    })
    return anomalies

def test_anomalies_json_exists():
    path = "/home/user/anomalies.json"
    assert os.path.isfile(path), f"Expected output file {path} does not exist."

def test_anomalies_json_content():
    csv_path = "/home/user/loc_metrics.csv"
    json_path = "/home/user/anomalies.json"

    assert os.path.isfile(csv_path), f"Input file {csv_path} is missing."
    expected_anomalies = get_expected_anomalies(csv_path)

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            actual_anomalies = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Failed to parse {json_path} as valid JSON: {e}"

    assert isinstance(actual_anomalies, list), f"Expected JSON root to be an array, got {type(actual_anomalies).__name__}."
    assert len(actual_anomalies) == len(expected_anomalies), f"Expected {len(expected_anomalies)} anomalies, but found {len(actual_anomalies)}."

    for i, (actual, expected) in enumerate(zip(actual_anomalies, expected_anomalies)):
        assert isinstance(actual, dict), f"Expected item at index {i} to be an object."
        assert "timestamp" in actual, f"Item at index {i} is missing 'timestamp'."
        assert "locale" in actual, f"Item at index {i} is missing 'locale'."
        assert "error_rate" in actual, f"Item at index {i} is missing 'error_rate'."

        assert actual["timestamp"] == expected["timestamp"], f"Mismatch in 'timestamp' at index {i}: expected {expected['timestamp']}, got {actual['timestamp']}."
        assert actual["locale"] == expected["locale"], f"Mismatch in 'locale' at index {i}: expected {expected['locale']}, got {actual['locale']}."

        # Compare error_rate with a small tolerance due to floating point representation in JSON
        diff = abs(actual["error_rate"] - expected["error_rate"])
        assert diff < 0.001, f"Mismatch in 'error_rate' at index {i}: expected {expected['error_rate']}, got {actual['error_rate']}."