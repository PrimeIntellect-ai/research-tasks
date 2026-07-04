# test_final_state.py

import os
import csv
import math
import pytest

def test_process_script_exists():
    script_path = "/home/user/process.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

def test_invalid_rows_log():
    raw_path = "/home/user/raw_tx.csv"
    invalid_path = "/home/user/invalid_rows.log"

    assert os.path.exists(raw_path), f"Raw data file {raw_path} is missing."
    assert os.path.exists(invalid_path), f"Output file {invalid_path} is missing."

    expected_invalid = []
    with open(raw_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) < 6:
                continue
            amount = float(row[3])
            currency = row[4]
            if amount <= 0 or currency not in ["USD", "EUR", "GBP"]:
                expected_invalid.append(",".join(row))

    with open(invalid_path, "r", encoding="utf-8") as f:
        actual_invalid = [line.strip() for line in f if line.strip()]

    assert expected_invalid == actual_invalid, f"Contents of {invalid_path} do not match expected invalid rows."

def test_summary_tsv():
    raw_path = "/home/user/raw_tx.csv"
    summary_path = "/home/user/summary.tsv"

    assert os.path.exists(summary_path), f"Output file {summary_path} is missing."

    rates = {"USD": 1.00, "EUR": 1.08, "GBP": 1.25}
    aggregated = {}

    with open(raw_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) < 6:
                continue
            amount = float(row[3])
            currency = row[4]
            if amount > 0 and currency in rates:
                email = row[2]
                email_parts = email.split("@")
                if len(email_parts) == 2:
                    masked_email = email_parts[0][0] + "***@" + email_parts[1]
                else:
                    masked_email = email

                usd_amount = amount * rates[currency]
                aggregated[masked_email] = aggregated.get(masked_email, 0.0) + usd_amount

    expected_summary = sorted(aggregated.items(), key=lambda x: x[1], reverse=True)

    with open(summary_path, "r", encoding="utf-8") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_summary), f"Expected {len(expected_summary)} lines in {summary_path}, found {len(actual_lines)}."

    for actual_line, (expected_email, expected_amount) in zip(actual_lines, expected_summary):
        parts = actual_line.split("\t")
        assert len(parts) == 2, f"Line in {summary_path} is not tab-separated: {actual_line}"
        assert parts[0] == expected_email, f"Expected masked email {expected_email}, got {parts[0]}"
        assert math.isclose(float(parts[1]), expected_amount, rel_tol=1e-5), f"Expected amount {expected_amount:.2f}, got {parts[1]}"

def test_pipeline_log():
    raw_path = "/home/user/raw_tx.csv"
    log_path = "/home/user/pipeline.log"

    assert os.path.exists(log_path), f"Output file {log_path} is missing."

    valid_count = 0
    invalid_count = 0

    with open(raw_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) < 6:
                continue
            amount = float(row[3])
            currency = row[4]
            if amount > 0 and currency in ["USD", "EUR", "GBP"]:
                valid_count += 1
            else:
                invalid_count += 1

    expected_log = f"[INFO] Processed {valid_count} valid records, dropped {invalid_count} invalid records."

    with open(log_path, "r", encoding="utf-8") as f:
        actual_log = f.read().strip()

    assert actual_log == expected_log, f"Expected log '{expected_log}', got '{actual_log}'"