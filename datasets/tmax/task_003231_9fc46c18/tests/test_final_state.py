# test_final_state.py

import os
import subprocess
import tempfile
import re
import shutil

SCRIPT_PATH = "/home/user/config_filter.py"
CLEAN_CORPUS = "/app/corpora/clean"
EVIL_CORPUS = "/app/corpora/evil"

def get_records(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if not content:
        return []
    # Split by the delimiter, keeping the delimiter if needed, but here we just split to count/evaluate
    records = content.split('---END RECORD---')
    # Remove trailing empty strings if any
    records = [r for r in records if r.strip()]
    return records

def is_evil(record):
    # The vulnerability is triggered when a block contains a `SetPrivilege: true` directive 
    # IMMEDIATELY followed by a `Timeout` directive with a value strictly greater than 9999.
    # We will search for SetPrivilege: true followed by Timeout: <val> ignoring other whitespace/newlines
    # "IMMEDIATELY followed by" implies no other directives in between, but newlines are fine.
    match = re.search(r'SetPrivilege:\s*true\s+Timeout:\s*(\d+)', record)
    if match:
        timeout_val = int(match.group(1))
        if timeout_val > 9999:
            return True
    return False

def test_config_filter_clean_corpus():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    with tempfile.TemporaryDirectory() as out_dir:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, CLEAN_CORPUS, out_dir],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Script failed on clean corpus:\n{result.stderr}"

        clean_files = []
        for root, _, files in os.walk(CLEAN_CORPUS):
            for file in files:
                if file.endswith('.log'):
                    clean_files.append(os.path.relpath(os.path.join(root, file), CLEAN_CORPUS))

        modified_clean = []
        for rel_file in clean_files:
            in_file = os.path.join(CLEAN_CORPUS, rel_file)
            out_file = os.path.join(out_dir, rel_file)

            if not os.path.exists(out_file):
                modified_clean.append(f"{rel_file} (missing)")
                continue

            with open(in_file, 'r', encoding='utf-8') as f1, open(out_file, 'r', encoding='utf-8') as f2:
                if f1.read() != f2.read():
                    modified_clean.append(f"{rel_file} (content mismatch)")

        if modified_clean:
            assert False, f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}"

def test_config_filter_evil_corpus():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    with tempfile.TemporaryDirectory() as out_dir:
        result = subprocess.run(
            ["python3", SCRIPT_PATH, EVIL_CORPUS, out_dir],
            capture_output=True, text=True
        )
        assert result.returncode == 0, f"Script failed on evil corpus:\n{result.stderr}"

        evil_files = []
        for root, _, files in os.walk(EVIL_CORPUS):
            for file in files:
                if file.endswith('.log'):
                    evil_files.append(os.path.relpath(os.path.join(root, file), EVIL_CORPUS))

        bypassed_evil = []
        for rel_file in evil_files:
            in_file = os.path.join(EVIL_CORPUS, rel_file)
            out_file = os.path.join(out_dir, rel_file)

            in_records = get_records(in_file)
            expected_clean_records = [r for r in in_records if not is_evil(r)]

            if not os.path.exists(out_file):
                if expected_clean_records:
                    bypassed_evil.append(f"{rel_file} (missing output but has clean records)")
                continue

            out_records = get_records(out_file)

            # Check if any evil records bypassed
            evil_in_out = [r for r in out_records if is_evil(r)]
            if evil_in_out:
                bypassed_evil.append(f"{rel_file} ({len(evil_in_out)} evil records bypassed)")
                continue

            # Check if clean records were preserved correctly
            if len(out_records) != len(expected_clean_records):
                bypassed_evil.append(f"{rel_file} (clean records count mismatch: expected {len(expected_clean_records)}, got {len(out_records)})")

        if bypassed_evil:
            assert False, f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed or malformed: {', '.join(bypassed_evil)}"