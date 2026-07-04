# test_final_state.py

import os
import stat
import subprocess
import re

def test_report_exists():
    """Test that the report.txt file exists."""
    file_path = "/home/user/report.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

def test_report_content():
    """Test that the report.txt file contains the correct values."""
    file_path = "/home/user/report.txt"
    with open(file_path, "r") as f:
        content = f.read()

    # Extract values using regex
    feature_match = re.search(r"Best Feature:\s*(.+)", content)
    slope_match = re.search(r"Slope:\s*([\d\.]+)", content)
    intercept_match = re.search(r"Intercept:\s*([\d\.]+)", content)
    mse_match = re.search(r"MSE:\s*([\d\.]+)", content)

    assert feature_match is not None, "Could not find 'Best Feature' in report.txt"
    assert slope_match is not None, "Could not find 'Slope' in report.txt"
    assert intercept_match is not None, "Could not find 'Intercept' in report.txt"
    assert mse_match is not None, "Could not find 'MSE' in report.txt"

    best_feature = feature_match.group(1).strip()
    slope = slope_match.group(1).strip()
    intercept = intercept_match.group(1).strip()
    mse = float(mse_match.group(1).strip())

    assert best_feature == "sensor_B", f"Expected Best Feature to be 'sensor_B', got '{best_feature}'"
    assert slope == "2.70", f"Expected Slope to be '2.70', got '{slope}'"
    assert intercept == "4.36", f"Expected Intercept to be '4.36', got '{intercept}'"

    # Accept 0.01, 0.02, or 0.03 for MSE due to floating point variations
    assert mse in [0.01, 0.02, 0.03], f"Expected MSE to be 0.01, 0.02, or 0.03, got '{mse}'"

def test_predict_script_exists_and_executable():
    """Test that predict.sh exists and is executable."""
    file_path = "/home/user/predict.sh"
    assert os.path.isfile(file_path), f"Script {file_path} is missing."

    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {file_path} is not executable."

def test_predict_script_output():
    """Test that predict.sh produces the correct output for a given input."""
    file_path = "/home/user/predict.sh"

    # Test case 1: x = 5.0 -> y = 2.70 * 5.0 + 4.36 = 17.86
    try:
        output1 = subprocess.check_output([file_path, "5.0"], text=True).strip()
    except subprocess.CalledProcessError as e:
        assert False, f"Execution of {file_path} failed: {e}"

    assert output1 == "17.86", f"Expected predict.sh 5.0 to output '17.86', got '{output1}'"

    # Test case 2: x = 10.0 -> y = 2.70 * 10.0 + 4.36 = 31.36
    try:
        output2 = subprocess.check_output([file_path, "10.0"], text=True).strip()
    except subprocess.CalledProcessError as e:
        assert False, f"Execution of {file_path} failed: {e}"

    assert output2 == "31.36", f"Expected predict.sh 10.0 to output '31.36', got '{output2}'"