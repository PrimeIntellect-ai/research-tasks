# test_final_state.py
import os
import re
import subprocess
import pytest

def test_experiment_fixed_script_exists():
    """Test that the corrected script was saved to the correct location."""
    file_path = "/home/user/experiment_fixed.py"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist. Did you save the corrected script?"

def test_fixed_metric_file_exists_and_correct():
    """Test that the fixed_metric.txt file exists and contains the correct accuracy."""
    file_path = "/home/user/fixed_metric.txt"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    # The expected output without data leakage is 0.5200
    assert content == "0.5200", f"Expected accuracy '0.5200', but found '{content}' in {file_path}."

def test_experiment_fixed_script_logic():
    """Test that the corrected script actually fixes the data leakage bug."""
    file_path = "/home/user/experiment_fixed.py"
    if not os.path.isfile(file_path):
        pytest.fail(f"Cannot check logic because {file_path} does not exist.")

    with open(file_path, "r") as f:
        content = f.read()

    # It should not do fit_transform on the whole X
    assert not re.search(r"scaler\.fit_transform\(\s*X\s*\)", content), "The script still fits the scaler on the entire dataset 'X'."

    # It should split X, not X_scaled
    assert re.search(r"train_test_split\(\s*X\s*,", content), "The script should split the original 'X', not the scaled version."

    # It should transform test data
    assert re.search(r"scaler\.transform\(", content), "The script does not appear to use scaler.transform() for the test set."

def test_experiment_fixed_script_execution():
    """Test that running the fixed script produces the correct output."""
    file_path = "/home/user/experiment_fixed.py"
    if not os.path.isfile(file_path):
        pytest.fail(f"Cannot execute {file_path} because it does not exist.")

    try:
        result = subprocess.run(
            ["python3", file_path],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        assert output == "0.5200", f"Running the fixed script produced '{output}' instead of expected '0.5200'."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running {file_path} failed with error:\n{e.stderr}")