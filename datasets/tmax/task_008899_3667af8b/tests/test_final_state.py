# test_final_state.py

import os
import subprocess
import pytest

def test_crash_payload_txt():
    path = "/home/user/crash_payload.txt"
    assert os.path.isfile(path), f"Expected file {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "UP AND RUNNING" in content, "crash_payload.txt does not contain the correct decoded payload that caused the crash."

def test_fuzzer_sh_exists_and_executable():
    path = "/home/user/fuzzer.sh"
    assert os.path.isfile(path), f"Expected file {path} does not exist."
    assert os.access(path, os.X_OK), f"Expected file {path} to be executable."

def test_monitor_sh_fixed_malicious_payload():
    path = "/home/user/monitor.sh"
    # "VVAgQU5EIFJVTk5JTkcK" decodes to "UP AND RUNNING\n"
    # The original script would crash with a bash syntax error because of word splitting.
    result = subprocess.run([path, "VVAgQU5EIFJVTk5JTkcK"], capture_output=True, text=True)

    assert result.returncode == 0, f"monitor.sh failed with exit code {result.returncode} on malicious payload."
    assert result.stderr.strip() == "", f"monitor.sh produced error output on malicious payload: {result.stderr}"
    assert "Service is DOWN" in result.stdout, "monitor.sh did not output 'Service is DOWN' for the malicious payload."

def test_monitor_sh_valid_payload():
    path = "/home/user/monitor.sh"
    # "VVA=" decodes to "UP"
    result = subprocess.run([path, "VVA="], capture_output=True, text=True)

    assert result.returncode == 0, f"monitor.sh failed with exit code {result.returncode} on valid payload."
    assert result.stderr.strip() == "", f"monitor.sh produced error output on valid payload: {result.stderr}"
    assert "Service is UP" in result.stdout, "monitor.sh did not output 'Service is UP' for the 'UP' payload."