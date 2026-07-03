# test_final_state.py

import os
import csv
import re
import subprocess
import pytest
import tempfile

EVIL_DIR = "/app/corpora/evil"
CLEAN_DIR = "/app/corpora/clean"
SCRIPT_PATH = "/home/user/sanitize.py"

SSN_REGEX = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
EMAIL_REGEX = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b')

def deduplicate_csv(input_path):
    """Helper to deduplicate a CSV by user_id, keeping the first occurrence."""
    seen_users = set()
    rows = []
    with open(input_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            user_id = row.get('user_id')
            if user_id not in seen_users:
                seen_users.add(user_id)
                rows.append(row)
    return rows

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Sanitize script not found at {SCRIPT_PATH}"

def test_evil_corpus_sanitized():
    """Check that evil corpus files are correctly deduplicated and sanitized."""
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    assert evil_files, "No CSV files found in evil corpus."

    bypassed_files = []

    for filename in evil_files:
        input_path = os.path.join(EVIL_DIR, filename)
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            output_path = tmp.name

        try:
            result = subprocess.run(
                ["python", SCRIPT_PATH, input_path, output_path],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                bypassed_files.append(f"{filename} (script crashed)")
                continue

            # Read output and verify
            expected_rows = deduplicate_csv(input_path)

            with open(output_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                out_rows = list(reader)

            if len(out_rows) != len(expected_rows):
                bypassed_files.append(f"{filename} (deduplication failed)")
                continue

            has_unmasked_pii = False
            for out_row in out_rows:
                feedback = out_row.get('feedback', '')
                if SSN_REGEX.search(feedback) or EMAIL_REGEX.search(feedback):
                    has_unmasked_pii = True
                    break

            if has_unmasked_pii:
                bypassed_files.append(filename)

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}")

def test_clean_corpus_preserved():
    """Check that clean corpus files are deduplicated but feedback is unchanged."""
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    assert clean_files, "No CSV files found in clean corpus."

    modified_files = []

    for filename in clean_files:
        input_path = os.path.join(CLEAN_DIR, filename)
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            output_path = tmp.name

        try:
            result = subprocess.run(
                ["python", SCRIPT_PATH, input_path, output_path],
                capture_output=True, text=True
            )
            if result.returncode != 0:
                modified_files.append(f"{filename} (script crashed)")
                continue

            expected_rows = deduplicate_csv(input_path)

            with open(output_path, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                out_rows = list(reader)

            if len(out_rows) != len(expected_rows):
                modified_files.append(f"{filename} (deduplication failed)")
                continue

            is_modified = False
            for exp_row, out_row in zip(expected_rows, out_rows):
                if exp_row.get('feedback') != out_row.get('feedback'):
                    is_modified = True
                    break

            if is_modified:
                modified_files.append(filename)

        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}")