# test_final_state.py
import os
import subprocess
import pytest
import glob
import re
from datetime import datetime

SCRIPT_PATH = "/home/user/filter_stream.sh"

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script at {SCRIPT_PATH} is not executable"

def parse_timestamp(ts_str):
    try:
        dt = datetime.strptime(ts_str, "%Y/%m/%d %H:%M:%S")
    except ValueError:
        try:
            dt = datetime.strptime(ts_str, "%d-%m-%Y %H:%M:%S")
        except ValueError:
            return None
    # datetime.timestamp() uses local timezone, matching bash `date -d`
    return int(dt.timestamp())

def test_adversarial_corpus():
    evil_dir = "/app/tests/corpus/evil"
    clean_dir = "/app/tests/corpus/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.log"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.log"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus: should output nothing
    for e_file in evil_files:
        with open(e_file, 'rb') as f:
            input_data = f.read()

        result = subprocess.run([SCRIPT_PATH], input=input_data, capture_output=True)
        if result.stdout.strip():
            evil_bypassed.append(os.path.basename(e_file))

    # Test clean corpus: should correctly transform timestamps and preserve payload
    for c_file in clean_files:
        with open(c_file, 'rb') as f:
            lines = f.read().splitlines()

        expected_lines = []
        for line in lines:
            if not line:
                continue
            line_str = line.decode('utf-8', errors='replace')
            m = re.match(r'^\[(.*?)\]\s*(.*)$', line_str)
            if m:
                ts, payload = m.groups()
                epoch = parse_timestamp(ts)
                if epoch is not None:
                    expected_lines.append(f"[{epoch}] {payload}".encode('utf-8'))
                else:
                    expected_lines.append(line)
            else:
                expected_lines.append(line)

        with open(c_file, 'rb') as f:
            input_data = f.read()

        result = subprocess.run([SCRIPT_PATH], input=input_data, capture_output=True)
        out_lines = result.stdout.splitlines()

        if out_lines != expected_lines:
            clean_modified.append(os.path.basename(c_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))