# test_final_state.py

import os
import stat
import subprocess
import json
import math
import pytest

PIPELINE_SCRIPT = "/home/user/pipeline.sh"
RAW_SENSORS = "/home/user/raw_sensors.csv"
CLEANED_SENSORS = "/home/user/cleaned_sensors.csv"
EXPERIMENTS_LOG = "/home/user/experiments.log"

@pytest.fixture(scope="session", autouse=True)
def run_pipeline():
    """Run the pipeline script before testing its outputs."""
    assert os.path.isfile(PIPELINE_SCRIPT), f"Missing script: {PIPELINE_SCRIPT}"

    st = os.stat(PIPELINE_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script is not executable: {PIPELINE_SCRIPT}"

    result = subprocess.run([PIPELINE_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}.\nStderr: {result.stderr}"

def test_cleaned_sensors_content():
    """Test that cleaned_sensors.csv contains the correct filtered rows."""
    assert os.path.isfile(CLEANED_SENSORS), f"Missing file: {CLEANED_SENSORS}"

    with open(CLEANED_SENSORS, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 8, f"Expected 1 header and 7 data rows, but got {len(lines)} lines."

    expected_header = "sensor_id,temp_c,pressure_hpa,vibration_hz"
    assert lines[0] == expected_header, f"Header mismatch: expected '{expected_header}', got '{lines[0]}'"

    expected_ids = {"1", "2", "5", "8", "9", "10", "11"}
    actual_ids = {line.split(',')[0] for line in lines[1:]}

    assert actual_ids == expected_ids, f"Cleaned data rows mismatch. Expected sensor IDs {expected_ids}, got {actual_ids}"

def test_experiments_log():
    """Test that experiments.log contains the correct JSON metadata."""
    assert os.path.isfile(EXPERIMENTS_LOG), f"Missing file: {EXPERIMENTS_LOG}"

    with open(EXPERIMENTS_LOG, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 1, "experiments.log is empty."

    last_line = lines[-1]
    try:
        log_entry = json.loads(last_line)
    except json.JSONDecodeError:
        pytest.fail(f"Last line of experiments.log is not valid JSON: {last_line}")

    assert "timestamp" in log_entry, "Missing 'timestamp' in log entry."
    assert "input_rows" in log_entry, "Missing 'input_rows' in log entry."
    assert "valid_rows" in log_entry, "Missing 'valid_rows' in log entry."
    assert "temp_pressure_correlation" in log_entry, "Missing 'temp_pressure_correlation' in log entry."

    assert log_entry["input_rows"] == 11, f"Expected input_rows=11, got {log_entry['input_rows']}"
    assert log_entry["valid_rows"] == 7, f"Expected valid_rows=7, got {log_entry['valid_rows']}"

    corr = log_entry["temp_pressure_correlation"]
    assert isinstance(corr, (int, float)), f"Correlation must be a number, got {type(corr)}"
    assert math.isclose(corr, -0.9922, abs_tol=0.0002), f"Expected correlation around -0.9922, got {corr}"