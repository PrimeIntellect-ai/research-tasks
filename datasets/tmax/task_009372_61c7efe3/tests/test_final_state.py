# test_final_state.py

import os
import subprocess
import csv
import pytest

@pytest.fixture(scope="session", autouse=True)
def execute_pipeline():
    """Run the bash script to ensure the pipeline is executed and outputs are generated."""
    script_path = "/home/user/run_experiments.sh"
    assert os.path.isfile(script_path), f"Bash script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Bash script {script_path} is not executable."

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error:\n{result.stderr}"

def test_experiment_log_exists_and_header():
    log_path = "/home/user/experiment_log.csv"
    assert os.path.isfile(log_path), f"Log file {log_path} was not created."

    with open(log_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        expected_header = ["dataset", "slope", "intercept", "removed_outliers"]
        assert header == expected_header, f"Incorrect header in {log_path}. Expected {expected_header}, got {header}."

def test_cleaned_data_files_created():
    expected_files = ['clean_sensor_A.csv', 'clean_sensor_B.csv', 'clean_sensor_C.csv']
    for f in expected_files:
        path = os.path.join('/home/user/cleaned_data', f)
        assert os.path.isfile(path), f"Cleaned data file {path} is missing."

def test_experiment_log_contents():
    log_path = "/home/user/experiment_log.csv"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 3, f"Expected exactly 3 data rows in {log_path}, found {len(rows)}."

    sensor_a = next((r for r in rows if r['dataset'] == 'sensor_A.csv'), None)
    assert sensor_a is not None, "Log entry for 'sensor_A.csv' not found in experiment_log.csv."

    try:
        slope = float(sensor_a['slope'])
        outliers = int(sensor_a['removed_outliers'])
    except ValueError as e:
        pytest.fail(f"Could not parse slope or outliers as numbers for sensor_A.csv: {e}")

    # Based on the deterministic generation script, slope should be around 2.5 and outliers exactly 4
    assert 2.0 < slope < 3.0, f"Calculated slope for sensor_A.csv is {slope}, expected a value around 2.5."
    assert outliers == 4, f"Removed outliers for sensor_A.csv is {outliers}, expected exactly 4."

def test_c_program_compilation_and_executable():
    c_source = "/home/user/cleaner.c"
    executable = "/home/user/cleaner"
    assert os.path.isfile(c_source), f"C source file {c_source} does not exist."
    assert os.path.isfile(executable), f"Compiled executable {executable} does not exist."
    assert os.access(executable, os.X_OK), f"Compiled binary {executable} is not executable."