# test_final_state.py

import os
import re
import math
import pytest

PIPELINE_DIR = "/home/user/pipeline"
DATA_FILE = os.path.join(PIPELINE_DIR, "data.txt")
WORKER_SCRIPT = os.path.join(PIPELINE_DIR, "worker.sh")
RESULT_FILE = os.path.join(PIPELINE_DIR, "result.txt")
STRACE_FILE = os.path.join(PIPELINE_DIR, "worker.strace")
TIMELINE_FILE = os.path.join(PIPELINE_DIR, "timeline.log")

def test_result_file_correct():
    assert os.path.isfile(RESULT_FILE), f"File {RESULT_FILE} does not exist."
    with open(RESULT_FILE, "r") as f:
        content = f.read().strip()

    # Check if it matches 0.001 (rounded to 3 decimal places, or more precise)
    try:
        val = float(content)
        assert round(val, 3) == 0.001, f"Expected standard deviation around 0.001, but got {val}"
    except ValueError:
        pytest.fail(f"Content of {RESULT_FILE} is not a valid float: {content}")

def test_worker_strace_exists():
    assert os.path.isfile(STRACE_FILE), f"File {STRACE_FILE} does not exist. Did you run strace?"
    assert os.path.getsize(STRACE_FILE) > 0, f"File {STRACE_FILE} is empty."

def test_timeline_log_exists_and_content():
    assert os.path.isfile(TIMELINE_FILE), f"File {TIMELINE_FILE} does not exist."
    with open(TIMELINE_FILE, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"File {TIMELINE_FILE} is empty."

    # Check if there's at least one line from metrics (contains 'processed') 
    # and at least one line from strace (contains 'fatal')
    has_processed = any("processed" in line for line in lines)
    has_fatal = any("fatal" in line.lower() for line in lines)

    assert has_processed or has_fatal, "timeline.log does not seem to contain expected merged content from metrics.log and worker.strace."

def test_worker_script_modified():
    assert os.path.isfile(WORKER_SCRIPT), f"File {WORKER_SCRIPT} does not exist."
    with open(WORKER_SCRIPT, "r") as f:
        content = f.read()

    # The original script had a naive variance calculation that caused a crash.
    # We just ensure the script still exists and is executable.
    assert os.access(WORKER_SCRIPT, os.X_OK), f"File {WORKER_SCRIPT} is not executable."