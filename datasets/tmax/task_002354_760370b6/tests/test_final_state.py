# test_final_state.py

import os
import csv
import subprocess
import tempfile
from collections import defaultdict
import pytest

PIPELINE_BIN = "/home/user/pipeline"
EVIL_CORPUS_DIR = "/opt/eval/evil"
CLEAN_CORPUS_DIR = "/opt/eval/clean"

def test_pipeline_binary_exists():
    assert os.path.exists(PIPELINE_BIN), f"Pipeline binary not found at {PIPELINE_BIN}"
    assert os.access(PIPELINE_BIN, os.X_OK), f"Pipeline binary at {PIPELINE_BIN} is not executable"

def run_pipeline(input_csv):
    fd, output_csv = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    try:
        result = subprocess.run(
            [PIPELINE_BIN, input_csv, output_csv],
            capture_output=True,
            text=True,
            timeout=10
        )
        assert result.returncode == 0, f"Pipeline failed on {input_csv} with exit code {result.returncode}\nStderr: {result.stderr}"

        with open(output_csv, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)
        return rows
    finally:
        if os.path.exists(output_csv):
            os.remove(output_csv)

def test_evil_corpus():
    if not os.path.exists(EVIL_CORPUS_DIR):
        pytest.skip(f"Evil corpus dir {EVIL_CORPUS_DIR} not found.")

    evil_files = [os.path.join(EVIL_CORPUS_DIR, f) for f in os.listdir(EVIL_CORPUS_DIR) if f.endswith(".csv")]
    assert evil_files, "No evil corpus files found."

    failed_files = []
    for evil_file in evil_files:
        output_rows = run_pipeline(evil_file)
        if len(output_rows) > 0:
            failed_files.append(os.path.basename(evil_file))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil bypassed: {', '.join(failed_files)}"

def test_clean_corpus():
    if not os.path.exists(CLEAN_CORPUS_DIR):
        pytest.skip(f"Clean corpus dir {CLEAN_CORPUS_DIR} not found.")

    clean_files = [os.path.join(CLEAN_CORPUS_DIR, f) for f in os.listdir(CLEAN_CORPUS_DIR) if f.endswith(".csv")]
    assert clean_files, "No clean corpus files found."

    failed_files = []
    for clean_file in clean_files:
        with open(clean_file, "r", encoding="utf-8") as f:
            input_rows = list(csv.reader(f))

        users = defaultdict(list)
        for row in input_rows:
            if len(row) >= 3:
                users[row[1]].append(row)

        expected_per_user = {}
        for user, rows in users.items():
            rows.sort(key=lambda x: int(x[0]))
            expected = []
            for i in range(len(rows)):
                if i > 0:
                    prev_t = int(rows[i-1][0])
                    curr_t = int(rows[i][0])
                    for t in range(prev_t + 1, curr_t):
                        expected.append([str(t), user, "[GAP]"])
                expected.append(rows[i])
            expected_per_user[user] = expected

        output_rows = run_pipeline(clean_file)

        actual_per_user = defaultdict(list)
        for row in output_rows:
            if len(row) >= 3:
                actual_per_user[row[1]].append(row)

        match = True
        if set(expected_per_user.keys()) != set(actual_per_user.keys()):
            match = False
        else:
            for user in expected_per_user:
                actual_user_rows = sorted(actual_per_user[user], key=lambda x: int(x[0]))
                if actual_user_rows != expected_per_user[user]:
                    match = False
                    break

        if not match:
            failed_files.append(os.path.basename(clean_file))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean modified or incorrectly gap-filled: {', '.join(failed_files)}"