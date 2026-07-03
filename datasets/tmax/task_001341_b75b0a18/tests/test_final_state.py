# test_final_state.py

import os
import json
import time
import subprocess
import pytest
from datetime import datetime

BINARY_PATH = "/home/user/backup_analyzer/target/release/backup_analyzer"
REPORT_PATH = "/home/user/report.jsonl"
THRESHOLD = 1.5

def test_binary_exists():
    """Test that the compiled Rust binary exists and is executable."""
    assert os.path.isfile(BINARY_PATH), f"Rust binary not found at {BINARY_PATH}. Did you compile in release mode?"
    assert os.access(BINARY_PATH, os.X_OK), f"Rust binary at {BINARY_PATH} is not executable."

def test_runtime_and_report_schema():
    """Test the runtime of the binary and validate the schema of the generated report."""
    # Remove existing report to ensure the binary creates a fresh one
    if os.path.exists(REPORT_PATH):
        os.remove(REPORT_PATH)

    start_time = time.time()
    result = subprocess.run([BINARY_PATH], capture_output=True)
    end_time = time.time()

    assert result.returncode == 0, f"Binary execution failed with return code {result.returncode}.\nStderr: {result.stderr.decode()}"

    runtime = end_time - start_time
    assert runtime < THRESHOLD, f"Runtime was {runtime:.3f}s, which exceeds the threshold of {THRESHOLD}s. Make sure you are using MongoDB aggregation pipelines."

    assert os.path.isfile(REPORT_PATH), f"Report file not created at {REPORT_PATH}"

    with open(REPORT_PATH, "r") as f:
        content = f.read().strip()

    if not content:
        pytest.fail(f"Report file {REPORT_PATH} is empty.")

    lines = content.split('\n')
    assert len(lines) == 500, f"Expected exactly 500 lines in the report, but got {len(lines)}."

    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} is not valid JSON: {line}")

        assert "job_id" in record and isinstance(record["job_id"], str), f"Line {i+1} missing or invalid 'job_id' (expected string)."
        assert "total_size_bytes" in record and isinstance(record["total_size_bytes"], (int, float)), f"Line {i+1} missing or invalid 'total_size_bytes' (expected number)."
        assert "completion_date" in record and isinstance(record["completion_date"], str), f"Line {i+1} missing or invalid 'completion_date' (expected string)."
        assert "is_archived" in record and isinstance(record["is_archived"], bool), f"Line {i+1} missing or invalid 'is_archived' (expected boolean)."

        # Check ISO8601 format for completion_date
        date_str = record["completion_date"].replace("Z", "+00:00")
        try:
            datetime.fromisoformat(date_str)
        except ValueError:
            pytest.fail(f"Line {i+1} has an invalid 'completion_date' format (expected ISO8601): {record['completion_date']}")