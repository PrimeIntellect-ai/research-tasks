# test_final_state.py

import os
import math
import subprocess
import pytest

def get_expected_stddev():
    data_path = "/home/user/risk_engine/data.txt"
    if not os.path.isfile(data_path):
        return None
    with open(data_path, 'r') as f:
        data = [float(line.strip()) for line in f.read().splitlines() if line.strip()]
    if not data:
        return None
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    return math.sqrt(variance)

def get_expected_secret():
    try:
        output = subprocess.check_output(['git', 'log', '-p'], cwd='/home/user/risk_engine', text=True)
        for line in output.splitlines():
            if 'CALIB_SECRET' in line and 'TRADEX' in line:
                parts = line.split('"')
                if len(parts) >= 3:
                    return parts[1]
    except Exception:
        pass
    return "TRADEX-9922-8811-SECRET"

def test_build_script_succeeds():
    build_script = "/home/user/risk_engine/build.sh"
    assert os.path.isfile(build_script), "build.sh is missing."
    result = subprocess.run(["./build.sh"], cwd="/home/user/risk_engine", capture_output=True, text=True)
    assert result.returncode == 0, f"build.sh failed to execute successfully. Error: {result.stderr}"

def test_calc_variance_executable_works():
    executable = "/home/user/risk_engine/calc_variance"
    assert os.path.isfile(executable), "calc_variance executable was not created."
    assert os.access(executable, os.X_OK), "calc_variance is not executable."

    result = subprocess.run(["./calc_variance"], cwd="/home/user/risk_engine", capture_output=True, text=True)
    assert result.returncode == 0, f"calc_variance failed to run. Error: {result.stderr}"

    output = result.stdout.strip()
    expected_stddev = get_expected_stddev()
    assert expected_stddev is not None, "data.txt is missing or empty, cannot compute expected stddev."

    try:
        output_val = float(output)
        assert math.isclose(output_val, expected_stddev, rel_tol=1e-3), \
            f"calc_variance output '{output_val}' does not match expected standard deviation '{expected_stddev:.4f}'"
    except ValueError:
        pytest.fail(f"calc_variance did not output a valid float. Output was: '{output}'")

def test_resolution_log_format_and_content():
    log_path = "/home/user/resolution.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    expected_secret = get_expected_secret()
    expected_stddev = get_expected_stddev()
    assert expected_stddev is not None, "data.txt is missing or empty."

    expected_content = f"SECRET: {expected_secret}\nSTDDEV: {expected_stddev:.4f}"

    assert content == expected_content, \
        f"{log_path} content is incorrect.\nExpected:\n{expected_content}\n\nGot:\n{content}"