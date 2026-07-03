# test_final_state.py
import os

def test_provision_script_exists():
    path = "/home/user/provision.exp"
    assert os.path.isfile(path), f"Verification failed: {path} not found."

def test_supervisor_script_exists():
    path = "/home/user/supervisor.sh"
    assert os.path.isfile(path), f"Verification failed: {path} not found."

def test_service_installed():
    path = "/home/user/service.sh"
    assert os.path.isfile(path), f"Verification failed: {path} not found. The app-installer.sh may not have been run successfully."
    assert os.access(path, os.X_OK), f"Verification failed: {path} is not executable."

def test_supervisor_log():
    path = "/home/user/supervisor.log"
    assert os.path.isfile(path), f"Verification failed: {path} not found."

    with open(path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 3, f"Verification failed: {path} should have exactly 3 lines, found {len(lines)}."

    expected_line = "[QUOTA ENFORCED] Restarted prod-worker"
    for i, line in enumerate(lines):
        assert line == expected_line, f"Verification failed: Log line {i+1} mismatch. Expected '{expected_line}', got '{line}'."