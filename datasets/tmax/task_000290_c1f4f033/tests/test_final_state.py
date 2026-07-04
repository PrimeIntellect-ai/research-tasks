# test_final_state.py

import os
import subprocess
import csv
import pytest
from collections import defaultdict

EXECUTABLE = "/home/user/etl_processor"
LOG_FILE = "/home/user/pipeline.log"
EVIL_CORPUS = "/app/corpus/evil/"
CLEAN_CORPUS = "/app/corpus/clean/"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def compute_expected_output(filepath):
    expected = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers = next(reader)

        symbols = []
        for i in range(1, len(headers), 2):
            sym = headers[i].replace('_price', '')
            symbols.append(sym)

        history = defaultdict(list)

        for row in reader:
            if not row:
                continue
            ts = row[0]
            for i, sym in enumerate(symbols):
                price_str = row[1 + i*2]
                vol_str = row[2 + i*2]
                if not price_str:
                    continue
                price = float(price_str)
                vol = vol_str

                history[sym].append(price)
                if len(history[sym]) > 3:
                    history[sym].pop(0)

                avg = sum(history[sym]) / len(history[sym])
                expected.append((ts, sym, price, vol, avg))

    return expected

def test_evil_corpus_rejected():
    evil_files = [os.path.join(EVIL_CORPUS, f) for f in os.listdir(EVIL_CORPUS) if f.endswith('.csv')]
    assert len(evil_files) > 0, "No evil files found to test."

    bypassed = []
    for filepath in evil_files:
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)

        if result.returncode != 1:
            bypassed.append((os.path.basename(filepath), "Exit code not 1"))
            continue

        if "REJECTED" not in result.stderr:
            bypassed.append((os.path.basename(filepath), "REJECTED not in stderr"))
            continue

        # Check log file
        if not os.path.isfile(LOG_FILE):
            bypassed.append((os.path.basename(filepath), f"Log file {LOG_FILE} missing"))
            continue

        with open(LOG_FILE, 'r') as f:
            log_content = f.read()

        expected_log = f"ERROR: Invalid encoding in file {filepath}"
        if expected_log not in log_content:
            bypassed.append((os.path.basename(filepath), "Missing expected log entry"))
            continue

    if bypassed:
        details = ", ".join(f"{f} ({r})" for f, r in bypassed)
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {details}")

def test_clean_corpus_accepted():
    clean_files = [os.path.join(CLEAN_CORPUS, f) for f in os.listdir(CLEAN_CORPUS) if f.endswith('.csv')]
    assert len(clean_files) > 0, "No clean files found to test."

    modified = []
    for filepath in clean_files:
        result = subprocess.run([EXECUTABLE, filepath], capture_output=True, text=True)

        if result.returncode != 0:
            modified.append((os.path.basename(filepath), f"Exit code {result.returncode} instead of 0"))
            continue

        stdout_lines = result.stdout.strip().split('\n')
        if not stdout_lines:
            modified.append((os.path.basename(filepath), "Empty output"))
            continue

        if stdout_lines[0].strip() != "timestamp,symbol,price,vol,rolling_avg_price":
            modified.append((os.path.basename(filepath), "Incorrect header"))
            continue

        expected_rows = compute_expected_output(filepath)
        actual_rows = stdout_lines[1:]

        if len(expected_rows) != len(actual_rows):
            modified.append((os.path.basename(filepath), f"Expected {len(expected_rows)} rows, got {len(actual_rows)}"))
            continue

        mismatch = False
        for expected, actual_line in zip(expected_rows, actual_rows):
            parts = actual_line.split(',')
            if len(parts) != 5:
                mismatch = True
                break

            ts, sym, price, vol, avg = expected
            a_ts, a_sym, a_price, a_vol, a_avg = parts

            if a_ts != ts or a_sym != sym or a_vol != vol:
                mismatch = True
                break

            try:
                if abs(float(a_price) - price) > 1e-4 or abs(float(a_avg) - avg) > 1e-4:
                    mismatch = True
                    break
            except ValueError:
                mismatch = True
                break

        if mismatch:
            modified.append((os.path.basename(filepath), "Output data mismatch"))

    if modified:
        details = ", ".join(f"{f} ({r})" for f, r in modified)
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/failed: {details}")