# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_detector_go_exists():
    path = "/home/user/detector.go"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_run_detector_script_exists_and_executable():
    path = "/home/user/run_detector.sh"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable by the owner."

def test_anomalies_output_correct():
    path = "/home/user/anomalies.out"
    assert os.path.exists(path), f"File {path} does not exist. Did you run your script manually?"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_lines = [
        "[2023-10-25T14:30:05Z] and [2023-10-25T14:30:06Z] - Similarity: 0.80",
        "[2023-10-25T14:30:20Z] and [2023-10-25T14:30:21Z] - Similarity: 1.00"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {path}, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch in {path}.\nExpected: {expected}\nActual:   {actual}"

def test_cron_job_configured():
    try:
        # Run crontab -l for the current user
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Is it configured for the user?")

    # Look for the specific script path in the crontab output
    script_path = "/home/user/run_detector.sh"
    has_job = False
    for line in crontab_output.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if script_path in line and line.startswith('* * * * *'):
            has_job = True
            break

    assert has_job, f"Could not find cron job '* * * * * {script_path}' in crontab."