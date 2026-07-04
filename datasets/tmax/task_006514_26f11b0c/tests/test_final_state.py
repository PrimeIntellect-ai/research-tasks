# test_final_state.py

import os
import csv
import hashlib
import subprocess
import pytest

PROCESSED_CSV = "/home/user/data/processed.csv"
INCOMING_CSV = "/home/user/data/incoming.csv"

def test_processed_file_exists():
    assert os.path.exists(PROCESSED_CSV), f"Expected output file {PROCESSED_CSV} does not exist."
    assert os.path.isfile(PROCESSED_CSV), f"Path {PROCESSED_CSV} is not a file."

def test_processed_file_utf8_encoding_and_content():
    # Read incoming data to derive expected output
    assert os.path.exists(INCOMING_CSV), f"Input file {INCOMING_CSV} is missing."
    with open(INCOMING_CSV, "r", encoding="cp1252", newline="") as f:
        incoming_rows = list(csv.DictReader(f))

    expected_rows = []
    for row in incoming_rows:
        expected_row = row.copy()

        # Masking email
        expected_row["email"] = hashlib.sha256(row["email"].encode("utf-8")).hexdigest()

        # Masking SSN
        ssn = row["ssn"]
        if len(ssn) >= 11 and ssn[3] == "-" and ssn[6] == "-":
            expected_row["ssn"] = f"***-**-{ssn[7:]}"

        # Imputing temperature
        if not row["temperature"].strip():
            expected_row["temperature"] = "98.6"

        expected_rows.append(expected_row)

    # Read processed data
    try:
        with open(PROCESSED_CSV, "r", encoding="utf-8", newline="") as f:
            processed_rows = list(csv.DictReader(f))
    except UnicodeDecodeError as e:
        pytest.fail(f"Output file {PROCESSED_CSV} is not valid UTF-8: {e}")

    assert len(processed_rows) == len(expected_rows), (
        f"Expected {len(expected_rows)} data rows, found {len(processed_rows)}"
    )

    for i, (proc_row, exp_row) in enumerate(zip(processed_rows, expected_rows)):
        assert proc_row["id"] == exp_row["id"], f"Row {i+1}: 'id' was altered."
        assert proc_row["name"] == exp_row["name"], f"Row {i+1}: 'name' was altered."
        assert proc_row["email"] == exp_row["email"], f"Row {i+1}: 'email' not correctly hashed."
        assert proc_row["ssn"] == exp_row["ssn"], f"Row {i+1}: 'ssn' not correctly masked. Got {proc_row['ssn']}"
        assert proc_row["temperature"] == exp_row["temperature"], f"Row {i+1}: 'temperature' not correctly imputed. Got {proc_row['temperature']}"
        assert proc_row["notes"] == exp_row["notes"], f"Row {i+1}: 'notes' do not match expected UTF-8 decoded text."

def test_cron_job_setup():
    try:
        crontab_output = subprocess.check_output(["crontab", "-l", "-u", "user"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("Could not read crontab for user 'user'.")

    # Look for the required schedule and script
    lines = [line.strip() for line in crontab_output.splitlines() if line.strip() and not line.strip().startswith("#")]

    cron_found = False
    for line in lines:
        if "15 3 * * *" in line and "clean_pipeline.py" in line:
            cron_found = True
            break

    assert cron_found, f"Cron job for clean_pipeline.py at 03:15 AM not correctly set up. Crontab contents:\n{crontab_output}"