# test_final_state.py

import os
import base64
import tempfile
import subprocess
import pytest

REPORT_FILE = "/home/user/analysis.txt"
BINARY_PATH = "/home/user/malware_repo/malware"
EXPECTED_SECRET = "gh0st_1n_th3_sh3ll"

def test_analysis_file_exists():
    assert os.path.isfile(REPORT_FILE), f"The report file {REPORT_FILE} does not exist."

def test_analysis_file_content():
    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n")]

    assert len(lines) == 2, f"Expected exactly 2 lines in {REPORT_FILE}, found {len(lines)}."

    secret = lines[0]
    assert secret == EXPECTED_SECRET, f"Line 1 (secret) is incorrect. Expected {EXPECTED_SECRET}, got {secret}."

    b64_payload = lines[1]
    try:
        raw_payload = base64.b64decode(b64_payload)
    except Exception as e:
        pytest.fail(f"Line 2 is not a valid base64 string: {e}")

    assert len(raw_payload) > 0, "Decoded payload is empty."

def test_payload_triggers_backdoor():
    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.read().strip().split("\n")]

    if len(lines) < 2:
        pytest.fail("Cannot run payload test: report file does not have 2 lines.")

    b64_payload = lines[1]
    try:
        raw_payload = base64.b64decode(b64_payload)
    except Exception:
        pytest.fail("Cannot run payload test: Line 2 is not valid base64.")

    assert os.path.isfile(BINARY_PATH), f"Target binary {BINARY_PATH} is missing."
    assert os.access(BINARY_PATH, os.X_OK), f"Target binary {BINARY_PATH} is not executable."

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(raw_payload)
        tmp_path = tmp.name

    try:
        result = subprocess.run(
            [BINARY_PATH, EXPECTED_SECRET, tmp_path],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout + result.stderr
        assert "Backdoor triggered!" in output, (
            "The payload did not trigger the backdoor. "
            f"Binary output was:\n{output}"
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The binary execution timed out. Your payload might have caused an infinite loop or hang.")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)