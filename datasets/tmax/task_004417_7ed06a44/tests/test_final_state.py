# test_final_state.py
import os
import subprocess
import pytest

def test_upload_handler_executable_exists():
    path = "/home/user/upload_handler"
    assert os.path.isfile(path), f"Executable {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_upload_handler_malicious_input():
    path = "/home/user/upload_handler"

    # Test with "../"
    result = subprocess.run([path, "../malicious.txt"], capture_output=True, text=True)
    assert result.returncode == 1, f"Expected exit code 1 for malicious input '../', got {result.returncode}"
    assert result.stdout == "ERR: Invalid filename\n", f"Expected exact stdout 'ERR: Invalid filename\\n' for '../', got {repr(result.stdout)}"

    # Test with "/"
    result2 = subprocess.run([path, "folder/file.txt"], capture_output=True, text=True)
    assert result2.returncode == 1, f"Expected exit code 1 for malicious input with '/', got {result2.returncode}"
    assert result2.stdout == "ERR: Invalid filename\n", f"Expected exact stdout 'ERR: Invalid filename\\n' for '/', got {repr(result2.stdout)}"

def test_upload_handler_safe_input():
    path = "/home/user/upload_handler"
    safe_filename = "safe_test_file.txt"
    expected_out_path = f"/home/user/uploads/{safe_filename}"

    if os.path.exists(expected_out_path):
        os.remove(expected_out_path)

    result = subprocess.run([path, safe_filename], capture_output=True, text=True)
    assert result.returncode == 0, f"Expected exit code 0 for safe input, got {result.returncode}. stderr: {result.stderr}"
    assert os.path.isfile(expected_out_path), f"Expected file {expected_out_path} to be created for safe input."

def test_redacted_alerts_log():
    traffic_log = "/home/user/traffic.log"
    redacted_log = "/home/user/redacted_alerts.log"

    assert os.path.isfile(traffic_log), f"{traffic_log} is missing."
    assert os.path.isfile(redacted_log), f"{redacted_log} is missing."

    with open(traffic_log, "r") as f:
        traffic_lines = f.read().splitlines()

    expected_redacted = []
    for line in traffic_lines:
        if "FILE: " in line:
            parts = line.split("FILE: ")
            if len(parts) > 1:
                file_part = parts[1].split(" ")[0]
                if "../" in file_part or "/" in file_part:
                    if " KEY: " in line:
                        prefix, key_val = line.split(" KEY: ", 1)
                        expected_redacted.append(f"{prefix} KEY: [REDACTED]")

    with open(redacted_log, "r") as f:
        actual_redacted = f.read().splitlines()

    assert actual_redacted == expected_redacted, (
        "The contents of redacted_alerts.log do not match the expected redacted malicious records.\n"
        f"Expected:\n{expected_redacted}\nGot:\n{actual_redacted}"
    )