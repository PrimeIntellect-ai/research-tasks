# test_final_state.py

import os
import csv
import json
import pytest

RAW_FILE = "/home/user/raw_data/transactions.csv"
SCRIPT_FILE = "/home/user/etl_pipeline.sh"
OUTPUT_DIR = "/home/user/etl_output"
MASKED_FILE = os.path.join(OUTPUT_DIR, "masked.csv")
ROLLING_FILE = os.path.join(OUTPUT_DIR, "rolling.csv")
SUMMARY_FILE = os.path.join(OUTPUT_DIR, "summary.json")

def read_raw_data():
    with open(RAW_FILE, "r") as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_FILE), f"Master script missing at {SCRIPT_FILE}"
    assert os.access(SCRIPT_FILE, os.X_OK), f"Master script {SCRIPT_FILE} is not executable."

def test_output_directory_exists():
    assert os.path.isdir(OUTPUT_DIR), f"Output directory missing at {OUTPUT_DIR}"

def test_masked_csv():
    assert os.path.isfile(MASKED_FILE), f"Masked file missing at {MASKED_FILE}"

    raw_data = read_raw_data()
    raw_data.sort(key=lambda x: int(x["timestamp"]))

    with open(MASKED_FILE, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["timestamp", "email", "ip", "amount", "category"], "Incorrect header in masked.csv"

        rows = list(reader)
        assert len(rows) == len(raw_data), f"Expected {len(raw_data)} rows in masked.csv, got {len(rows)}"

        for i, (actual_row, expected_dict) in enumerate(zip(rows, raw_data)):
            ts, email, ip, amt, cat = actual_row

            # Check timestamp, amount, category
            assert ts == expected_dict["timestamp"], f"Row {i+1}: Timestamp mismatch"
            assert amt == expected_dict["amount"], f"Row {i+1}: Amount mismatch"
            assert cat == expected_dict["category"], f"Row {i+1}: Category mismatch"

            # Check email masking
            orig_email = expected_dict["email"]
            orig_user, orig_domain = orig_email.split("@")
            expected_email = f"{orig_user[0]}***@{orig_domain}"
            assert email == expected_email, f"Row {i+1}: Email masking incorrect. Expected {expected_email}, got {email}"

            # Check IP masking
            orig_ip = expected_dict["ip"]
            ip_parts = orig_ip.split(".")
            expected_ip = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0"
            assert ip == expected_ip, f"Row {i+1}: IP masking incorrect. Expected {expected_ip}, got {ip}"

def test_rolling_csv():
    assert os.path.isfile(ROLLING_FILE), f"Rolling file missing at {ROLLING_FILE}"

    raw_data = read_raw_data()
    raw_data.sort(key=lambda x: int(x["timestamp"]))

    category_history = {}
    expected_rolling = []

    for row in raw_data:
        cat = row["category"]
        amt = float(row["amount"])
        if cat not in category_history:
            category_history[cat] = []
        category_history[cat].append(amt)

        window = category_history[cat][-3:]
        rolling_avg = sum(window) / len(window)
        expected_rolling.append((row["timestamp"], cat, f"{rolling_avg:.2f}"))

    with open(ROLLING_FILE, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["timestamp", "category", "rolling_avg"], "Incorrect header in rolling.csv"

        rows = list(reader)
        assert len(rows) == len(expected_rolling), f"Expected {len(expected_rolling)} rows in rolling.csv, got {len(rows)}"

        for i, (actual, expected) in enumerate(zip(rows, expected_rolling)):
            assert tuple(actual) == expected, f"Row {i+1}: Rolling average mismatch. Expected {expected}, got {tuple(actual)}"

def test_summary_json():
    assert os.path.isfile(SUMMARY_FILE), f"Summary file missing at {SUMMARY_FILE}"

    raw_data = read_raw_data()

    category_stats = {}
    for row in raw_data:
        cat = row["category"]
        amt = float(row["amount"])
        if cat not in category_stats:
            category_stats[cat] = []
        category_stats[cat].append(amt)

    with open(SUMMARY_FILE, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("summary.json contains invalid JSON")

    for cat, amounts in category_stats.items():
        assert cat in summary, f"Category '{cat}' missing from summary.json"

        expected_total = sum(amounts)
        expected_avg = expected_total / len(amounts)

        actual_total = float(summary[cat]["total"])
        actual_avg = float(summary[cat]["avg"])

        assert abs(actual_total - expected_total) < 0.01, f"Total for {cat} mismatch. Expected {expected_total:.2f}, got {actual_total}"
        assert abs(actual_avg - expected_avg) < 0.01, f"Average for {cat} mismatch. Expected {expected_avg:.2f}, got {actual_avg}"