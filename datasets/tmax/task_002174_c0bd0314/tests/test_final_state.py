# test_final_state.py

import os
import pytest

def test_verification_log_exists_and_correct():
    log_path = "/home/user/verification.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist. The end-to-end script likely failed or was not run."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "E2E_SUCCESS: Valid payload and exit code received."
    assert content == expected, f"Verification log content is incorrect. Expected '{expected}', got '{content}'."

def test_payload_bin_exists_and_executable():
    bin_path = "/home/user/payload_bin"
    assert os.path.exists(bin_path), f"Executable {bin_path} does not exist. The Makefile may not have built it correctly."
    assert os.access(bin_path, os.X_OK), f"File {bin_path} is not executable."

def test_makefile_exists():
    makefile_path = "/home/user/Makefile"
    assert os.path.exists(makefile_path), f"Makefile at {makefile_path} does not exist."

def test_run_e2e_exists_and_executable():
    script_path = "/home/user/run_e2e.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_notify_script_exists():
    notify_path = "/home/user/notify.py"
    assert os.path.exists(notify_path), f"Script {notify_path} does not exist."

def test_payload_s_exists():
    payload_s_path = "/home/user/payload.s"
    assert os.path.exists(payload_s_path), f"Assembly file {payload_s_path} does not exist."

    with open(payload_s_path, "r") as f:
        content = f.read()

    assert "_start" in content, f"The assembly file {payload_s_path} is missing the _start symbol."