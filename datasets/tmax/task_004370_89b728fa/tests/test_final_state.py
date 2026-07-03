# test_final_state.py

import os
import subprocess
import pytest

CLEAN_DIR = "/app/corpora/clean"
EVIL_DIR = "/app/corpora/evil"
SANITIZER_BIN = "/home/user/sanitizer"
MAKEFILE_PATH = "/app/vendored/libcsv_etl/Makefile"

def process_csv(input_lines):
    if not input_lines:
        return ""
    header = input_lines[0].strip()
    output = [header]
    seen_tx_ids = set()
    rolling_window = []

    for line in input_lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if len(parts) != 5:
            continue
        timestamp, tx_id, card_number, amount_str, status = parts

        if status not in ("SUCCESS", "PENDING"):
            continue

        if tx_id in seen_tx_ids:
            continue

        try:
            amount = float(amount_str)
        except ValueError:
            continue

        # Calculate rolling average if we include this amount
        test_window = rolling_window + [amount]
        if len(test_window) > 3:
            test_window = test_window[-3:]

        if sum(test_window) / len(test_window) > 5000.0:
            continue

        # Accept record
        seen_tx_ids.add(tx_id)
        rolling_window = test_window

        if len(card_number) == 16:
            masked_card = "*" * 12 + card_number[-4:]
        else:
            masked_card = card_number

        output.append(f"{timestamp},{tx_id},{masked_card},{amount_str},{status}")

    return "\n".join(output) + "\n"

def test_makefile_fixed():
    assert os.path.isfile(MAKEFILE_PATH), f"Makefile missing at {MAKEFILE_PATH}"
    with open(MAKEFILE_PATH, "r") as f:
        content = f.read()
    assert "-DSIMULATE_RETRY_DUPLICATION=1" not in content, "The perturbation in the Makefile was not removed."

def test_sanitizer_binary_exists():
    assert os.path.isfile(SANITIZER_BIN), f"Sanitizer binary not found at {SANITIZER_BIN}"
    assert os.access(SANITIZER_BIN, os.X_OK), f"Sanitizer binary at {SANITIZER_BIN} is not executable"

def test_clean_corpus():
    failed_files = []
    total = 0
    for fname in sorted(os.listdir(CLEAN_DIR)):
        if not fname.endswith(".csv"):
            continue
        total += 1
        fpath = os.path.join(CLEAN_DIR, fname)
        with open(fpath, "r") as f:
            input_data = f.read()

        expected_output = process_csv(input_data.strip().split("\n"))

        proc = subprocess.run([SANITIZER_BIN], input=input_data, text=True, capture_output=True)
        if proc.returncode != 0 or proc.stdout.strip() != expected_output.strip():
            failed_files.append(fname)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total} clean modified: {', '.join(failed_files)}")

def test_evil_corpus():
    failed_files = []
    total = 0
    for fname in sorted(os.listdir(EVIL_DIR)):
        if not fname.endswith(".csv"):
            continue
        total += 1
        fpath = os.path.join(EVIL_DIR, fname)
        with open(fpath, "r") as f:
            input_data = f.read()

        expected_output = process_csv(input_data.strip().split("\n"))

        proc = subprocess.run([SANITIZER_BIN], input=input_data, text=True, capture_output=True)
        if proc.returncode != 0 or proc.stdout.strip() != expected_output.strip():
            failed_files.append(fname)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total} evil bypassed: {', '.join(failed_files)}")