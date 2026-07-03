# test_final_state.py

import os
import math
import subprocess
import pytest

TICKET_DIR = "/home/user/ticket_4092"

def test_hidden_config_file():
    config_path = os.path.join(TICKET_DIR, ".calib_secret_v2")
    assert os.path.isfile(config_path), f"Hidden configuration file {config_path} is missing. Did you trace the system calls?"

    with open(config_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {config_path} is not a valid float: {content}")

    assert math.isclose(val, 2.5), f"Expected value in {config_path} to be 2.5, got {val}"

def test_clean_results_csv():
    results_path = os.path.join(TICKET_DIR, "clean_results.csv")
    assert os.path.isfile(results_path), f"Output file {results_path} is missing. Did you run the script?"

    with open(results_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, f"{results_path} is empty."

    # Extract data lines and the final volatility line
    data_lines = [line.strip() for line in lines if not line.startswith("#") and line.strip()]
    final_line = [line.strip() for line in lines if line.startswith("# FINAL_CALIBRATED_VOLATILITY:")]

    assert len(final_line) == 1, "Missing or multiple FINAL_CALIBRATED_VOLATILITY lines in clean_results.csv"

    # Check parsed clean prices
    # Expected clean prices from prices.csv: 100.0, 101.5, 103.0, 102.5, 105.2
    expected_prices = [100.0, 101.5, 103.0, 102.5, 105.2]
    actual_prices = []

    # Skip header
    for line in data_lines[1:]:
        parts = line.split(',')
        if len(parts) >= 2:
            try:
                actual_prices.append(float(parts[1]))
            except ValueError:
                pass

    assert actual_prices == expected_prices, f"Cleaned prices do not match expected. Got: {actual_prices}, Expected: {expected_prices}"

    # Check calculated volatility
    # Calculate expected volatility
    returns = [math.log(expected_prices[i] / expected_prices[i-1]) for i in range(1, len(expected_prices))]
    mean_return = sum(returns) / len(returns)
    variance = sum((u - mean_return)**2 for u in returns) / (len(returns) - 1)
    volatility = math.sqrt(variance * 252)
    expected_calibrated = volatility * 2.5

    # Extract actual calculated volatility
    try:
        actual_calibrated = float(final_line[0].split(":")[1].strip())
    except (IndexError, ValueError):
        pytest.fail(f"Could not parse final volatility from line: {final_line[0]}")

    assert math.isclose(actual_calibrated, expected_calibrated, rel_tol=1e-4), \
        f"Calibrated volatility is incorrect. Expected ~{expected_calibrated:.6f}, got {actual_calibrated:.6f}"

def test_regression_test_script():
    test_script_path = os.path.join(TICKET_DIR, "test_pricing.py")
    assert os.path.isfile(test_script_path), f"Regression test script {test_script_path} is missing."

    # Run the test script
    result = subprocess.run(
        ["python3", "-m", "unittest", test_script_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Regression test script failed to run successfully.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_venv_exists():
    venv_path = os.path.join(TICKET_DIR, "venv")
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} is missing."

    # Check if pip/python exists in venv
    python_path = os.path.join(venv_path, "bin", "python")
    assert os.path.isfile(python_path) or os.path.isfile(os.path.join(venv_path, "Scripts", "python.exe")), \
        "Python executable not found in virtual environment."