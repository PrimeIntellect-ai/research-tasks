# test_final_state.py

import os
import subprocess
import tempfile
import pytest

EXECUTABLE = "/home/user/filter"
CLEAN_DIR = "/app/corpus/clean"
EVIL_DIR = "/app/corpus/evil"

def test_executable_exists():
    assert os.path.isfile(EXECUTABLE), f"Executable not found at {EXECUTABLE}"
    assert os.access(EXECUTABLE, os.X_OK), f"File at {EXECUTABLE} is not executable"

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_DIR) if f.endswith('.csv')]
    assert evil_files, f"No CSV files found in {EVIL_DIR}"

    bypassed_files = []

    for f in evil_files:
        input_path = os.path.join(EVIL_DIR, f)
        with tempfile.NamedTemporaryFile(delete=False) as out_csv, \
             tempfile.NamedTemporaryFile(delete=False) as log_txt:
            out_path = out_csv.name
            log_path = log_txt.name

        try:
            result = subprocess.run(
                [EXECUTABLE, input_path, out_path, log_path],
                capture_output=True,
                text=True
            )
            if result.returncode != 1:
                bypassed_files.append(f)
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)
            if os.path.exists(log_path):
                os.remove(log_path)

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {bypassed_files}")

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_DIR) if f.endswith('.csv')]
    assert clean_files, f"No CSV files found in {CLEAN_DIR}"

    failed_files = []

    for f in clean_files:
        input_path = os.path.join(CLEAN_DIR, f)
        with tempfile.NamedTemporaryFile(delete=False) as out_csv, \
             tempfile.NamedTemporaryFile(delete=False) as log_txt:
            out_path = out_csv.name
            log_path = log_txt.name

        try:
            result = subprocess.run(
                [EXECUTABLE, input_path, out_path, log_path],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                failed_files.append(f"{f} (exit code {result.returncode})")
                continue

            # verify output
            with open(input_path, 'r') as infile:
                in_lines = infile.read().splitlines()

            with open(out_path, 'r') as outfile:
                out_lines = outfile.read().splitlines()

            # deduplicate logic manually
            seen = set()
            expected_out = []
            expected_logs = []

            if in_lines:
                expected_out.append(in_lines[0]) # header
                for line in in_lines[1:]:
                    if not line.strip():
                        continue
                    parts = line.split(',')
                    tid = parts[0]
                    if tid not in seen:
                        seen.add(tid)
                        expected_out.append(line)
                    else:
                        expected_logs.append(f"Duplicate Dropped: {tid}")

            if out_lines != expected_out:
                failed_files.append(f"{f} (output mismatch)")
                continue

            with open(log_path, 'r') as logfile:
                log_lines = logfile.read().splitlines()

            if log_lines != expected_logs:
                failed_files.append(f"{f} (log mismatch)")
                continue

        finally:
            if os.path.exists(out_path):
                os.remove(out_path)
            if os.path.exists(log_path):
                os.remove(log_path)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {len(clean_files)} clean modified/failed: {failed_files}")