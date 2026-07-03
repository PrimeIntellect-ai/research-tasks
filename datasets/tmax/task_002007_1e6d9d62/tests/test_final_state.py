# test_final_state.py
import os
import json
import csv
from datetime import datetime, timezone
from collections import defaultdict

def parse_iso8601(time_str):
    # Python 3.7+ fromisoformat handles some, but let's use a robust approach or datetime.fromisoformat if available.
    # Since Python 3.11, fromisoformat handles "Z" and offsets well. 
    # Let's just use datetime.fromisoformat.
    # If it fails, fallback to manual parsing.
    try:
        dt = datetime.fromisoformat(time_str)
    except ValueError:
        # Simple fallback for standard formats if needed, but fromisoformat should work for setup data
        dt = datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S%z")
    return dt.astimezone(timezone.utc)

def compute_expected_summary():
    europe_file = "/home/user/locales/europe_logs.json"
    asia_file = "/home/user/locales/asia_logs.csv"

    counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    if os.path.exists(europe_file):
        with open(europe_file, "r") as f:
            europe_data = json.load(f)
            for row in europe_data:
                dt = parse_iso8601(row["time"])
                bucket = dt.strftime("%Y-%m-%dT%H:00:00Z")
                counts[bucket][row["locale"]][row["msg_id"]] += 1

    if os.path.exists(asia_file):
        with open(asia_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                dt = datetime.fromtimestamp(int(row["timestamp"]), tz=timezone.utc)
                bucket = dt.strftime("%Y-%m-%dT%H:00:00Z")
                counts[bucket][row["locale"]][row["msg_id"]] += 1

    summary = []
    for bucket in sorted(counts.keys()):
        for locale in sorted(counts[bucket].keys()):
            msg_counts = counts[bucket][locale]
            # Sort by count descending, then msg_id ascending
            top_msg_id = sorted(msg_counts.items(), key=lambda x: (-x[1], x[0]))[0]
            summary.append({
                "hour": bucket,
                "locale": locale,
                "top_msg_id": top_msg_id[0],
                "count": top_msg_id[1]
            })

    return summary

def test_output_file_exists():
    assert os.path.isfile("/home/user/locales/hourly_summary.json"), "Output file /home/user/locales/hourly_summary.json is missing."

def test_output_content_is_correct():
    output_file = "/home/user/locales/hourly_summary.json"
    assert os.path.isfile(output_file), "Cannot test content because output file is missing."

    with open(output_file, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            assert False, "Output file is not valid JSON."

    expected_data = compute_expected_summary()

    assert isinstance(actual_data, list), "Output must be a JSON array."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual.get("hour") == expected["hour"], f"Item {i}: expected hour {expected['hour']}, got {actual.get('hour')}"
        assert actual.get("locale") == expected["locale"], f"Item {i}: expected locale {expected['locale']}, got {actual.get('locale')}"
        assert actual.get("top_msg_id") == expected["top_msg_id"], f"Item {i}: expected top_msg_id {expected['top_msg_id']}, got {actual.get('top_msg_id')}"
        assert actual.get("count") == expected["count"], f"Item {i}: expected count {expected['count']}, got {actual.get('count')}"