# test_final_state.py

import os
import csv
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

def get_expected_output(raw_logs_path):
    expected_rows = []
    with open(raw_logs_path, "r", encoding="utf-8", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            log_msg = row.get("log_message", "")
            if not log_msg:
                continue
            cleaned_msg = log_msg.replace("\n", " ")
            if not cleaned_msg:
                continue
            distance = levenshtein(cleaned_msg, "SYSTEM_STARTUP_SEQUENCE_INITIATED")
            expected_rows.append({
                "timestamp": int(row["timestamp"]),
                "user_id": row["user_id"],
                "cleaned_log_message": cleaned_msg,
                "distance": distance
            })

    expected_rows.sort(key=lambda x: x["timestamp"])

    for i, row in enumerate(expected_rows):
        if i == 0:
            row["is_anomaly"] = 0
        else:
            prev_dist = expected_rows[i-1]["distance"]
            if abs(row["distance"] - prev_dist) > 10:
                row["is_anomaly"] = 1
            else:
                row["is_anomaly"] = 0

    return expected_rows

def test_c_source_exists():
    assert os.path.isfile("/home/user/clean_logs.c"), "The C source file /home/user/clean_logs.c is missing."

def test_executable_exists():
    assert os.path.isfile("/home/user/clean_logs"), "The compiled executable /home/user/clean_logs is missing."
    assert os.access("/home/user/clean_logs", os.X_OK), "/home/user/clean_logs is not executable."

def test_cleaned_logs_correctness():
    raw_logs_path = "/home/user/raw_logs.csv"
    cleaned_logs_path = "/home/user/cleaned_logs.csv"

    assert os.path.isfile(cleaned_logs_path), f"The output file {cleaned_logs_path} is missing."

    expected_data = get_expected_output(raw_logs_path)

    actual_data = []
    with open(cleaned_logs_path, "r", encoding="utf-8", newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            assert len(row) == 5, f"Expected 5 columns in output, got {len(row)} in row: {row}"
            actual_data.append({
                "timestamp": int(row[0]),
                "user_id": row[1],
                "cleaned_log_message": row[2],
                "distance": int(row[3]),
                "is_anomaly": int(row[4])
            })

    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} rows in output, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual["timestamp"] == expected["timestamp"], f"Row {i+1}: expected timestamp {expected['timestamp']}, got {actual['timestamp']}"
        assert actual["user_id"] == expected["user_id"], f"Row {i+1}: expected user_id {expected['user_id']}, got {actual['user_id']}"
        assert actual["cleaned_log_message"] == expected["cleaned_log_message"], f"Row {i+1}: expected message '{expected['cleaned_log_message']}', got '{actual['cleaned_log_message']}'"
        assert actual["distance"] == expected["distance"], f"Row {i+1}: expected distance {expected['distance']}, got {actual['distance']}"
        assert actual["is_anomaly"] == expected["is_anomaly"], f"Row {i+1}: expected is_anomaly {expected['is_anomaly']}, got {actual['is_anomaly']}"