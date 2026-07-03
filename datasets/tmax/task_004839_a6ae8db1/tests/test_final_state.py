# test_final_state.py
import os
import json
import pytest

INPUT_FILE = "/home/user/telemetry.csv"
OUTPUT_FILE = "/home/user/processed_locales.jsonl"

def compute_expected_data(input_path):
    expected = []
    locale_latencies = {}

    with open(input_path, "rb") as f:
        lines = f.read().strip().split(b'\n')

    for line in lines:
        if not line:
            continue
        parts = line.split(b',', 4)
        if len(parts) != 5:
            continue

        timestamp_raw = parts[0].decode('ascii')
        locale = parts[1].decode('ascii')
        encoding = parts[2].decode('ascii')
        latency = float(parts[3].decode('ascii'))
        message_raw = parts[4]

        # 1. Timestamp alignment
        # 2023-10-12T08:15:32Z -> 2023-10-12T08:15:00Z
        aligned_time = timestamp_raw[:17] + "00Z"

        # 2. Character encoding handling
        if encoding == "ISO-8859-1":
            message_utf8 = message_raw.decode('iso-8859-1')
        else:
            message_utf8 = message_raw.decode('utf-8')

        # 3. Rolling statistics computation
        if locale not in locale_latencies:
            locale_latencies[locale] = []
        locale_latencies[locale].append(latency)

        # Keep only the last 3 events
        recent_latencies = locale_latencies[locale][-3:]
        rolling_avg = sum(recent_latencies) / len(recent_latencies)
        rolling_avg_rounded = round(rolling_avg, 2)

        expected.append({
            "aligned_time": aligned_time,
            "locale": locale,
            "rolling_avg_latency": rolling_avg_rounded,
            "message_utf8": message_utf8
        })

    return expected

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist."
    assert os.path.isfile(OUTPUT_FILE), f"Expected {OUTPUT_FILE} to be a file."

def test_output_file_contents():
    assert os.path.exists(INPUT_FILE), f"Input file {INPUT_FILE} is missing, cannot compute expected state."

    expected_data = compute_expected_data(INPUT_FILE)

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == len(expected_data), f"Expected {len(expected_data)} JSON lines, but found {len(lines)}."

    for i, (line, expected_obj) in enumerate(zip(lines, expected_data)):
        try:
            actual_obj = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

        assert "aligned_time" in actual_obj, f"Line {i+1} missing 'aligned_time' key."
        assert "locale" in actual_obj, f"Line {i+1} missing 'locale' key."
        assert "rolling_avg_latency" in actual_obj, f"Line {i+1} missing 'rolling_avg_latency' key."
        assert "message_utf8" in actual_obj, f"Line {i+1} missing 'message_utf8' key."

        assert actual_obj["aligned_time"] == expected_obj["aligned_time"], f"Line {i+1} aligned_time mismatch."
        assert actual_obj["locale"] == expected_obj["locale"], f"Line {i+1} locale mismatch."
        assert actual_obj["message_utf8"] == expected_obj["message_utf8"], f"Line {i+1} message_utf8 mismatch."

        # Check rolling average with tolerance for float rounding
        actual_avg = float(actual_obj["rolling_avg_latency"])
        expected_avg = expected_obj["rolling_avg_latency"]
        assert abs(actual_avg - expected_avg) < 0.015, (
            f"Line {i+1} rolling_avg_latency mismatch: expected ~{expected_avg}, got {actual_avg}"
        )