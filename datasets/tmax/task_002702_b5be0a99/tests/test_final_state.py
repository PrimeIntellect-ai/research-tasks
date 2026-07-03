# test_final_state.py

import os
import subprocess
import csv
import io
import pytest

SCRIPT_PATH = "/home/user/preprocess.py"
EVIL_DIR = "/app/data/evil/"
CLEAN_DIR = "/app/data/clean/"

def run_script(input_csv_content):
    process = subprocess.Popen(
        ["python3", SCRIPT_PATH],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=input_csv_content)
    return stdout, stderr, process.returncode

def parse_csv(content):
    reader = csv.DictReader(io.StringIO(content))
    return list(reader), reader.fieldnames

def check_continuous_timestamps_and_ffill(rows):
    if not rows:
        return True, "Empty CSV"

    try:
        prev_ts = int(rows[0]['timestamp'])
        prev_price = float(rows[0]['price'])
    except ValueError:
        return False, "Invalid timestamp or price in first row"

    for i in range(1, len(rows)):
        row = rows[i]
        try:
            ts = int(row['timestamp'])
            price = float(row['price'])
        except ValueError:
            return False, f"Invalid timestamp or price in row {i+1}"

        if ts != prev_ts + 1:
            return False, f"Timestamps not continuous: {prev_ts} to {ts}"

        if row['tx_id'] == 'GAP':
            if row['comment'] != 'FILLED':
                return False, f"GAP row has wrong comment: {row['comment']}"
            if price != prev_price:
                return False, f"GAP row price not forward-filled. Expected {prev_price}, got {price}"

        prev_ts = ts
        prev_price = price

    return True, ""

def check_no_newlines(content):
    # Check if there are any newlines inside fields
    # A simple way is to check if the number of lines in the raw string
    # equals the number of rows + 1 (for header), assuming no trailing newline issues.
    reader = csv.reader(io.StringIO(content))
    rows = list(reader)
    if not content.endswith('\n') and content != "":
        lines_count = content.count('\n') + 1
    else:
        lines_count = content.count('\n')

    if lines_count != len(rows):
        return False, f"Embedded newlines detected. Lines: {lines_count}, CSV rows: {len(rows)}"
    return True, ""

def check_logging(stderr_content, rows):
    logs = stderr_content.strip().split('\n')
    logs = [l for l in logs if l.strip()]
    if len(logs) != len(rows):
        return False, f"Expected {len(rows)} log lines, got {len(logs)}"

    prices = []
    for i, row in enumerate(rows):
        try:
            ts = int(row['timestamp'])
            price = float(row['price'])
        except ValueError:
            return False, f"Invalid timestamp or price in row {i+1}"

        prices.append(price)
        window = prices[-3:]
        avg = sum(window) / len(window)
        expected_log = f"LOG: {ts} {avg:.2f}"

        if logs[i] != expected_log:
            return False, f"Log mismatch at row {i+1}. Expected '{expected_log}', got '{logs[i]}'"

    return True, ""

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_evil_corpus():
    if not os.path.isdir(EVIL_DIR):
        pytest.skip(f"Evil directory {EVIL_DIR} not found")

    files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    failed_files = []

    for f in files:
        file_path = os.path.join(EVIL_DIR, f)
        with open(file_path, 'r') as infile:
            content = infile.read()

        stdout, stderr, rc = run_script(content)
        if rc != 0:
            failed_files.append(f"{f} (Script crashed)")
            continue

        rows, fieldnames = parse_csv(stdout)
        if fieldnames != ['timestamp', 'tx_id', 'price', 'comment']:
            failed_files.append(f"{f} (Invalid headers)")
            continue

        nl_ok, nl_msg = check_no_newlines(stdout)
        if not nl_ok:
            failed_files.append(f"{f} ({nl_msg})")
            continue

        ts_ok, ts_msg = check_continuous_timestamps_and_ffill(rows)
        if not ts_ok:
            failed_files.append(f"{f} ({ts_msg})")
            continue

        log_ok, log_msg = check_logging(stderr, rows)
        if not log_ok:
            failed_files.append(f"{f} ({log_msg})")
            continue

        # Check deduplication
        tx_ids = [r['tx_id'] for r in rows if r['tx_id'] != 'GAP']
        if len(tx_ids) != len(set(tx_ids)):
            failed_files.append(f"{f} (Duplicate tx_ids found)")
            continue

    assert not failed_files, f"{len(failed_files)} of {len(files)} evil bypassed: " + ", ".join(failed_files)

def test_clean_corpus():
    if not os.path.isdir(CLEAN_DIR):
        pytest.skip(f"Clean directory {CLEAN_DIR} not found")

    files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    failed_files = []

    for f in files:
        file_path = os.path.join(CLEAN_DIR, f)
        with open(file_path, 'r') as infile:
            content = infile.read()

        stdout, stderr, rc = run_script(content)
        if rc != 0:
            failed_files.append(f"{f} (Script crashed)")
            continue

        rows, fieldnames = parse_csv(stdout)
        orig_rows, orig_fieldnames = parse_csv(content)

        if rows != orig_rows:
            failed_files.append(f"{f} (Clean data modified)")
            continue

        log_ok, log_msg = check_logging(stderr, rows)
        if not log_ok:
            failed_files.append(f"{f} ({log_msg})")
            continue

    assert not failed_files, f"{len(failed_files)} of {len(files)} clean modified: " + ", ".join(failed_files)