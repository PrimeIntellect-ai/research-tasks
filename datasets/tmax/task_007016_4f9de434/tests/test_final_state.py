# test_final_state.py
import os

def test_script_exists():
    script_path = "/home/user/scan_artifacts.py"
    assert os.path.isfile(script_path), f"Expected script at {script_path} does not exist."

def test_malicious_paths_file_exists():
    log_path = "/home/user/malicious_paths.txt"
    assert os.path.isfile(log_path), f"Expected output file at {log_path} does not exist."

def test_malicious_paths_content():
    log_path = "/home/user/malicious_paths.txt"
    expected_paths = {
        "../../etc/shadow",
        "/root/.ssh/authorized_keys",
        "bin/../../var/run/daemon.pid"
    }

    with open(log_path, "r") as f:
        actual_paths = set(line.strip() for line in f if line.strip())

    assert actual_paths == expected_paths, (
        f"The contents of {log_path} are incorrect.\n"
        f"Expected: {expected_paths}\n"
        f"Actual: {actual_paths}"
    )