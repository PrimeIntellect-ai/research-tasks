# test_final_state.py
import os
import subprocess
import pytest

def test_recovered_token_file():
    token_file = "/home/user/recovered_token.txt"
    assert os.path.isfile(token_file), f"FAIL: Token file missing at {token_file}"

    with open(token_file, "r") as f:
        token = f.read().strip()

    assert token == "SEC-8f7a9b2d4c", f"FAIL: Incorrect token recovered. Expected 'SEC-8f7a9b2d4c', got '{token}'"

def test_compute_mean_output():
    script_path = "/home/user/metrics_build/compute_mean.sh"
    assert os.path.isfile(script_path), f"FAIL: Script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"FAIL: Script {script_path} is not executable"

    result = subprocess.run(
        ["bash", script_path],
        capture_output=True,
        text=True,
        cwd="/home/user/metrics_build"
    )

    assert result.returncode == 0, f"FAIL: Script {script_path} failed to execute properly."

    output = result.stdout.strip()
    assert output == "0.222222222", f"FAIL: Precision test failed. Expected '0.222222222', got '{output}'"

def test_build_success_log():
    log_file = "/home/user/build_success.log"
    assert os.path.isfile(log_file), f"FAIL: Log file missing at {log_file}. Did you run test_build.sh?"

    with open(log_file, "r") as f:
        content = f.read()

    assert "BUILD OK" in content, f"FAIL: {log_file} does not contain 'BUILD OK'"