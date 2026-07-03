# test_final_state.py

import os
import json
import csv
from datetime import datetime, timezone

def parse_csv_timestamp(ts_str):
    # Format: DD/MM/YYYY HH:MM:SS
    dt = datetime.strptime(ts_str, "%d/%m/%Y %H:%M:%S")
    dt = dt.replace(tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def parse_epoch_timestamp(epoch_int):
    dt = datetime.fromtimestamp(epoch_int, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def normalize_locale(loc_str):
    return loc_str.lower().replace("_", "-")

def compute_expected_data():
    eu_logs_path = "/home/user/loc_data/eu_logs.csv"
    asia_logs_path = "/home/user/loc_data/asia_logs.json"

    records = {}

    if os.path.exists(eu_logs_path):
        with open(eu_logs_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                ts = parse_csv_timestamp(row["timestamp"])
                loc = normalize_locale(row["lang_code"])
                key = row["translation_key"]
                count = int(row["usage_count"])

                group_key = (ts, loc, key)
                if group_key not in records or records[group_key] < count:
                    records[group_key] = count

    if os.path.exists(asia_logs_path):
        with open(asia_logs_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for item in data:
                ts = parse_epoch_timestamp(item["time_logged"])
                loc = normalize_locale(item["locale"])
                key = item["key"]
                count = int(item["uses"])

                group_key = (ts, loc, key)
                if group_key not in records or records[group_key] < count:
                    records[group_key] = count

    expected_list = []
    for (ts, loc, key), count in records.items():
        expected_list.append({
            "timestamp": ts,
            "locale": loc,
            "key": key,
            "usage_count": count
        })

    expected_list.sort(key=lambda x: (x["timestamp"], x["locale"], x["key"]))
    return expected_list

def test_normalized_timeseries_exists():
    output_path = "/home/user/normalized_timeseries.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

def test_normalized_timeseries_content():
    output_path = "/home/user/normalized_timeseries.jsonl"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    actual_data = []
    with open(output_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                actual_data.append(obj)
            except json.JSONDecodeError:
                assert False, f"Line {line_num} in {output_path} is not valid JSON."

    expected_data = compute_expected_data()

    assert len(actual_data) == len(expected_data), \
        f"Expected {len(expected_data)} records, but found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, \
            f"Record at index {i} mismatch.\nExpected: {expected}\nActual: {actual}"

def test_normalized_timeseries_schema():
    output_path = "/home/user/normalized_timeseries.jsonl"
    if not os.path.isfile(output_path):
        return

    with open(output_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)

            assert set(obj.keys()) == {"timestamp", "locale", "key", "usage_count"}, \
                f"Line {line_num} has incorrect fields: {list(obj.keys())}"

            assert isinstance(obj["timestamp"], str), f"Line {line_num}: timestamp must be a string"
            assert isinstance(obj["locale"], str), f"Line {line_num}: locale must be a string"
            assert isinstance(obj["key"], str), f"Line {line_num}: key must be a string"
            assert isinstance(obj["usage_count"], int), f"Line {line_num}: usage_count must be an integer"

            assert obj["timestamp"].endswith("Z") and "T" in obj["timestamp"], \
                f"Line {line_num}: timestamp is not in RFC3339 UTC format"
            assert obj["locale"] == obj["locale"].lower(), \
                f"Line {line_num}: locale must be strictly lowercase"
            assert "_" not in obj["locale"], \
                f"Line {line_num}: locale must use hyphen instead of underscore"