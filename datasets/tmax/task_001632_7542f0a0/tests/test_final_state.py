# test_final_state.py

import os
import csv
import json
import pytest

def get_expected_data():
    input_file = "/home/user/config_events.log"
    assert os.path.isfile(input_file), f"Input file {input_file} is missing."

    events = []
    with open(input_file, "r") as f:
        for line in f:
            if not line.strip():
                continue
            ts, srv, key, added, removed = line.strip().split("|")
            events.append({
                "ts": ts,
                "srv": srv,
                "key": key,
                "net": int(added) - int(removed)
            })

    # Sort by CONFIG_KEY alphabetically, then TIMESTAMP ascending
    events.sort(key=lambda x: (x["key"], x["ts"]))

    history = {}
    expected_csv = []
    max_abs_avg = -1
    max_key = ""

    for e in events:
        k = e["key"]
        if k not in history:
            history[k] = []
        history[k].append(e["net"])

        window = history[k][-3:]
        # Truncate towards zero for integer division
        avg = int(sum(window) / len(window))

        expected_csv.append(f"{e['ts']},{e['srv']},{e['key']},{e['net']},{avg}")

        abs_avg = abs(avg)
        if abs_avg > max_abs_avg:
            max_abs_avg = abs_avg
            max_key = k
        elif abs_avg == max_abs_avg:
            if k < max_key:
                max_key = k

    return expected_csv, max_key, max_abs_avg

def test_csv_output():
    expected_csv, _, _ = get_expected_data()

    csv_file = "/home/user/rolling_averages.csv"
    assert os.path.isfile(csv_file), f"Output file {csv_file} is missing. The script did not generate it."

    with open(csv_file, "r") as f:
        actual_csv = [line.strip() for line in f if line.strip()]

    assert len(actual_csv) == len(expected_csv), f"Expected {len(expected_csv)} lines in CSV, but got {len(actual_csv)}."

    for i, (actual, expected) in enumerate(zip(actual_csv, expected_csv)):
        assert actual == expected, f"Mismatch at line {i + 1} in {csv_file}.\nExpected: {expected}\nGot:      {actual}"

def test_json_output():
    _, expected_max_key, expected_max_abs_avg = get_expected_data()

    json_file = "/home/user/max_volatility.json"
    assert os.path.isfile(json_file), f"Output file {json_file} is missing. The script did not generate it."

    with open(json_file, "r") as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_file} does not contain valid JSON.")

    assert "max_key" in actual_json, f"JSON output is missing the 'max_key' field."
    assert "max_abs_avg" in actual_json, f"JSON output is missing the 'max_abs_avg' field."

    assert actual_json["max_key"] == expected_max_key, f"Expected max_key '{expected_max_key}', got '{actual_json['max_key']}'."
    assert actual_json["max_abs_avg"] == expected_max_abs_avg, f"Expected max_abs_avg {expected_max_abs_avg}, got {actual_json['max_abs_avg']}."