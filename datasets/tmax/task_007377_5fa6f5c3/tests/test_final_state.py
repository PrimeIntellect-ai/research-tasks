# test_final_state.py
import os
import subprocess

def test_bad_commit():
    expected_file = "/tmp/expected_bad_commit.txt"
    actual_file = "/home/user/bad_commit.txt"

    assert os.path.isfile(actual_file), f"File {actual_file} is missing."

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected bad commit hash '{expected_hash}', but got '{actual_hash}' in {actual_file}."

def test_poison_line():
    actual_file = "/home/user/poison_line.txt"
    assert os.path.isfile(actual_file), f"File {actual_file} is missing."

    with open(actual_file, "r") as f:
        actual_line = f.read().strip()

    assert actual_line == "742", f"Expected poison line '742', but got '{actual_line}' in {actual_file}."

def test_monitor_fixed():
    fixed_script = "/home/user/monitor_fixed.sh"
    log_file = "/home/user/logs/yesterday.log"

    assert os.path.isfile(fixed_script), f"File {fixed_script} is missing."
    assert os.access(fixed_script, os.X_OK), f"File {fixed_script} is not executable."

    try:
        result = subprocess.run(
            [fixed_script, log_file],
            capture_output=True,
            text=True,
            timeout=5
        )
    except subprocess.TimeoutExpired:
        assert False, f"Execution of {fixed_script} timed out after 5 seconds. The script might still contain an infinite loop."

    assert result.returncode == 0, f"{fixed_script} exited with non-zero exit code {result.returncode}. Stderr: {result.stderr}"
    assert "Alerts found: 1" in result.stdout, f"Expected output to contain 'Alerts found: 1', but got: {result.stdout}"