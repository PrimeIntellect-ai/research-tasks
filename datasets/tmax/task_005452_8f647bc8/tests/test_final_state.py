# test_final_state.py

import os
import json
import csv
import pytest

CORRUPT_LOG_PATH = "/home/user/corrupt_lines.log"
BILLING_SUMMARY_PATH = "/home/user/billing_summary.json"
APP_LOGS_PATH = "/home/user/app_logs.csv"

def test_corrupt_lines_log():
    assert os.path.isfile(CORRUPT_LOG_PATH), f"File {CORRUPT_LOG_PATH} is missing."

    expected_corrupt_lines = []

    with open(APP_LOGS_PATH, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for i, row in enumerate(reader, start=2):
            try:
                float(row[2])
                float(row[3])
            except ValueError:
                expected_corrupt_lines.append(str(i))

    with open(CORRUPT_LOG_PATH, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_corrupt_lines, (
        f"Contents of {CORRUPT_LOG_PATH} are incorrect. "
        f"Expected {expected_corrupt_lines}, got {actual_lines}."
    )

def test_billing_summary_json():
    assert os.path.isfile(BILLING_SUMMARY_PATH), f"File {BILLING_SUMMARY_PATH} is missing."

    expected_billing = {}
    with open(APP_LOGS_PATH, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                b = float(row['bytes'])
                d = float(row['duration'])
                user = row['user_id']
                cost = (b / 1048576.0) * 0.02 + (d * 0.005)
                expected_billing[user] = expected_billing.get(user, 0.0) + cost
            except ValueError:
                continue

    for user in expected_billing:
        expected_billing[user] = round(expected_billing[user], 4)

    with open(BILLING_SUMMARY_PATH, 'r') as f:
        try:
            actual_billing = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {BILLING_SUMMARY_PATH} is not a valid JSON.")

    assert actual_billing == expected_billing, (
        f"Contents of {BILLING_SUMMARY_PATH} are incorrect. "
        f"Expected {expected_billing}, got {actual_billing}."
    )