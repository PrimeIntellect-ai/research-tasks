# test_final_state.py

import os
import re
import stat
import subprocess
import pytest

SCRIPT_PATH = "/home/user/deploy_and_monitor.sh"
METRICS_PATH = "/home/user/metrics.csv"

@pytest.fixture(scope="session", autouse=True)
def run_script():
    """Run the student's script before checking the state."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

    # Check if executable
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

    # Run the script
    result = subprocess.run([SCRIPT_PATH], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

def test_script_exists_and_executable():
    """Verify the script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_metrics_file_exists():
    """Verify the metrics.csv file is created."""
    assert os.path.isfile(METRICS_PATH), f"Metrics file {METRICS_PATH} was not created."

def test_metrics_file_content():
    """Verify the content of metrics.csv."""
    with open(METRICS_PATH, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 lines in {METRICS_PATH}, found {len(lines)}."

    header = lines[0]
    assert header == "TIMESTAMP,PID,RSS_KB", f"Incorrect header in {METRICS_PATH}: {header}"

    data_pattern = re.compile(r"^[0-9]+,[0-9]+,[0-9]+$")
    for i, line in enumerate(lines[1:], start=1):
        assert data_pattern.match(line), f"Line {i+1} in {METRICS_PATH} does not match expected format: {line}"

def test_processes_cleaned_up():
    """Verify that python3 and socat processes were gracefully terminated."""
    # Check python3
    python_check = subprocess.run(["pgrep", "-f", "python3 -m http.server 8443"], capture_output=True, text=True)
    assert python_check.returncode != 0, "python3 http.server process was not cleaned up."

    # Check socat
    socat_check = subprocess.run(["pgrep", "-f", "socat.*9443"], capture_output=True, text=True)
    assert socat_check.returncode != 0, "socat process was not cleaned up."