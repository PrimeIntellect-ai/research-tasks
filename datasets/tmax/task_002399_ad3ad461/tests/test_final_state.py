# test_final_state.py
import os
import sys
import json
import subprocess
import pytest

APP_DIR = "/home/user/app"
EVENT_PROCESSOR_FILE = "/home/user/app/event_processor.py"
FUZZ_TEST_FILE = "/home/user/fuzz_test.py"
MRE_FILE = "/home/user/mre.py"
REPORT_FILE = "/home/user/incident_report.txt"

def test_event_processor_fixed():
    assert os.path.isfile(EVENT_PROCESSOR_FILE), f"File {EVENT_PROCESSOR_FILE} is missing."

    # Dynamically import the module
    sys.path.insert(0, APP_DIR)
    try:
        from event_processor import run_batch
    except ImportError as e:
        pytest.fail(f"Failed to import run_batch from event_processor: {e}")
    finally:
        sys.path.pop(0)

    # Run the batch to check if the race condition is fixed
    num_events = 1000
    events = [json.dumps({"user": "test", "amount": 1}) for _ in range(num_events)]
    stats = run_batch(events)

    assert stats.get("test") == num_events, (
        f"Race condition still exists: expected {num_events}, got {stats.get('test')}"
    )

def test_fuzz_test_script():
    assert os.path.isfile(FUZZ_TEST_FILE), f"File {FUZZ_TEST_FILE} is missing."

    result = subprocess.run([sys.executable, FUZZ_TEST_FILE], capture_output=True, text=True)
    assert result.returncode == 0, f"fuzz_test.py failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_mre_script():
    assert os.path.isfile(MRE_FILE), f"File {MRE_FILE} is missing."

    with open(MRE_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) < 35, f"mre.py has {len(lines)} lines, which is 35 or more."

def test_incident_report():
    assert os.path.isfile(REPORT_FILE), f"File {REPORT_FILE} is missing."

    with open(REPORT_FILE, 'r', encoding='utf-8') as f:
        content = f.read().strip().lower()

    assert "lock" in content or "rlock" in content, (
        f"Incident report does not contain the correct concurrency primitive name. Content: {content}"
    )