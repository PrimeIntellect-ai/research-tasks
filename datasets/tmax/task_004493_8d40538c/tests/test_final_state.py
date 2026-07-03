# test_final_state.py

import os
import json
import re
import subprocess
from pathlib import Path
import pytest

CLEANER_SCRIPT = "/home/user/cleaner.py"
CLEAN_CORPUS_DIR = Path("/home/user/corpora/clean")
EVIL_CORPUS_DIR = Path("/home/user/corpora/evil")

def normalize_msg(msg: str) -> str:
    msg = msg.lower()
    return re.sub(r'[^a-z0-9\s]', '', msg)

def is_valid_line(line: str) -> bool:
    try:
        # If the line has raw invalid unicode escapes, json.loads might succeed but return surrogates
        # However, we also need to check if it's valid JSON
        data = json.loads(line)
    except json.JSONDecodeError:
        return False

    if not isinstance(data, dict):
        return False

    for key in ['ts', 'sensor_id', 'msg']:
        if key not in data:
            return False
        if not isinstance(data[key], str):
            return False

    # Check for surrogate characters (invalid unicode)
    for value in data.values():
        if isinstance(value, str):
            if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
                return False

    return True

def get_expected_output(filepath: Path) -> list:
    valid_records = []
    with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if is_valid_line(line):
                # We know it parses successfully
                data = json.loads(line)
                data['msg'] = normalize_msg(data['msg'])
                valid_records.append(data)

    valid_records.sort(key=lambda x: x['ts'])
    return valid_records

def run_cleaner(filepath: Path) -> list:
    result = subprocess.run(
        ["python3", CLEANER_SCRIPT, str(filepath)],
        capture_output=True,
        text=True,
        check=False
    )
    if result.returncode != 0:
        raise RuntimeError(f"Script failed on {filepath.name}:\n{result.stderr}")

    output_lines = result.stdout.strip().split('\n')
    records = []
    for line in output_lines:
        if line.strip():
            records.append(json.loads(line))
    return records

def test_cleaner_script_exists():
    assert os.path.isfile(CLEANER_SCRIPT), f"Cleaner script not found at {CLEANER_SCRIPT}"

def test_clean_corpus():
    clean_files = list(CLEAN_CORPUS_DIR.glob("*.jsonl"))
    assert clean_files, "No clean corpus files found."

    failed_files = []
    for filepath in clean_files:
        try:
            expected = get_expected_output(filepath)
            actual = run_cleaner(filepath)
            if expected != actual:
                failed_files.append(filepath.name)
        except Exception as e:
            failed_files.append(f"{filepath.name} (Error: {e})")

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified incorrectly or failed: {failed_files}"

def test_evil_corpus():
    evil_files = list(EVIL_CORPUS_DIR.glob("*.jsonl"))
    assert evil_files, "No evil corpus files found."

    failed_files = []
    for filepath in evil_files:
        try:
            expected = get_expected_output(filepath)
            actual = run_cleaner(filepath)
            if expected != actual:
                failed_files.append(filepath.name)
        except Exception as e:
            failed_files.append(f"{filepath.name} (Error: {e})")

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed or failed: {failed_files}"