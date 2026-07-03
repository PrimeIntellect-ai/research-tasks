# test_final_state.py

import os
import subprocess
import tempfile
import re
import pytest

BINARY_PATH = "/home/user/pipeline/target/release/filter"
CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"

def test_cron_job_configured():
    # Run setup_cron.sh first to ensure it's applied if it wasn't already run manually
    setup_script = "/home/user/setup_cron.sh"
    assert os.path.isfile(setup_script), f"Setup script missing at {setup_script}"

    # Execute the setup script
    subprocess.run(["bash", setup_script], check=True)

    # Check crontab
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    crontab_output = result.stdout.strip()

    pattern = r"^0\s+\*\s+\*\s+\*\s+\*\s+/home/user/pipeline/target/release/filter\s+/var/data/incoming\.csv\s+/var/data/clean\.csv"

    match_found = any(re.match(pattern, line.strip()) for line in crontab_output.splitlines())
    assert match_found, f"Cron job not correctly configured. Current crontab:\n{crontab_output}"

def test_rust_binary_exists():
    assert os.path.isfile(BINARY_PATH), f"Rust binary missing at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Rust binary at {BINARY_PATH} is not executable"

def count_csv_rows(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return sum(1 for _ in f)

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith('.csv')]
    failed_files = []

    for filename in clean_files:
        input_path = os.path.join(CLEAN_CORPUS_DIR, filename)
        original_rows = count_csv_rows(input_path)

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            output_path = tmp.name

        try:
            subprocess.run([BINARY_PATH, input_path, output_path], check=True, capture_output=True)
            output_rows = count_csv_rows(output_path)
            if output_rows != original_rows:
                failed_files.append((filename, original_rows, output_rows))
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if failed_files:
        details = ", ".join([f"{f} (expected {e}, got {g})" for f, e, g in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected: {details}")

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith('.csv')]
    failed_files = []

    for filename in evil_files:
        input_path = os.path.join(EVIL_CORPUS_DIR, filename)

        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            output_path = tmp.name

        try:
            subprocess.run([BINARY_PATH, input_path, output_path], check=True, capture_output=True)
            output_rows = count_csv_rows(output_path)
            # Expecting exactly 1 row (the header)
            if output_rows != 1:
                failed_files.append((filename, output_rows))
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if failed_files:
        details = ", ".join([f"{f} (got {g} rows, expected 1)" for f, g in failed_files])
        pytest.fail(f"{len(failed_files)} of {len(evil_files)} evil files bypassed: {details}")