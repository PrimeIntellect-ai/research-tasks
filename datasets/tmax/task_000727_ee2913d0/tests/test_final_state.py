# test_final_state.py
import os
import re
import pytest

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def get_expected_summary(raw_data_path):
    valid_sensors = ["alpha_sensor", "beta_sensor", "gamma_sensor"]
    pattern = re.compile(r"^([0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}),([a-zA-Z_]+),([0-9]+(\.[0-9]+)?)$")

    parsed_rows = []
    prev_row = None

    with open(raw_data_path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            match = pattern.match(line)
            if not match:
                continue

            timestamp = match.group(1)
            sensor_id_raw = match.group(2)
            value = float(match.group(3))

            # Map sensor
            min_dist = float('inf')
            mapped_sensor = None
            for vs in valid_sensors:
                dist = levenshtein(sensor_id_raw, vs)
                if dist < min_dist:
                    min_dist = dist
                    mapped_sensor = vs

            if min_dist > 2:
                continue

            current_row = (timestamp, mapped_sensor, value)

            if prev_row == current_row:
                continue

            parsed_rows.append(current_row)
            prev_row = current_row

    # Group and aggregate
    buckets = {}
    for ts, sensor, val in parsed_rows:
        bucketed_hour = ts[:14] + "00:00"
        key = (bucketed_hour, sensor)
        if key not in buckets:
            buckets[key] = []
        buckets[key].append(val)

    expected_lines = []
    for key in sorted(buckets.keys()):
        bucketed_hour, sensor = key
        vals = buckets[key]
        avg_val = sum(vals) / len(vals)
        expected_lines.append(f"[{bucketed_hour}] {sensor} AVG:{avg_val:.2f}")

    return expected_lines

def test_c_source_exists():
    assert os.path.exists("/home/user/etl_processor.c"), "/home/user/etl_processor.c does not exist."

def test_c_binary_exists_and_executable():
    assert os.path.exists("/home/user/etl_processor"), "/home/user/etl_processor does not exist."
    assert os.access("/home/user/etl_processor", os.X_OK), "/home/user/etl_processor is not executable."

def test_summary_txt_correct():
    raw_data_path = "/home/user/raw_data.csv"
    summary_path = "/home/user/summary.txt"

    assert os.path.exists(raw_data_path), f"{raw_data_path} is missing."
    assert os.path.exists(summary_path), f"{summary_path} was not generated."

    expected_lines = get_expected_summary(raw_data_path)

    with open(summary_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {summary_path} do not match the expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )