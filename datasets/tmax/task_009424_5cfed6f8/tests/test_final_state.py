# test_final_state.py

import os
import stat
import pytest

def test_pipeline_script_exists_and_executable():
    """Check if the pipeline script exists and is executable."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Missing script file: {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable by the user."

def test_reduced_data_csv():
    """Check if reduced_data.csv was created and dropped the zero-variance column."""
    file_path = "/home/user/reduced_data.csv"
    assert os.path.isfile(file_path), f"Missing intermediate dataset: {file_path}"

    with open(file_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"File {file_path} is empty."

    header = lines[0].strip().split(",")
    assert "id" in header, "Column 'id' is missing in reduced_data.csv"
    assert "is_anomaly" in header, "Column 'is_anomaly' is missing in reduced_data.csv"
    assert "sensor_1" not in header, "Column 'sensor_1' has zero variance and should have been dropped."
    assert "sensor_3" in header, "Column 'sensor_3' has variance and should be kept."

def test_best_model_txt():
    """Check if best_model.txt contains the correct output."""
    file_path = "/home/user/best_model.txt"
    assert os.path.isfile(file_path), f"Missing output file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "Best Threshold: 42"
    assert content == expected_content, f"Expected content '{expected_content}' in {file_path}, but found '{content}'"