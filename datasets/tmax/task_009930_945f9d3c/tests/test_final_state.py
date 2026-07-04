# test_final_state.py

import os
import re
import math
import subprocess
import pytest

BASE_DIR = "/home/user/mc_pricer"

def test_makefile_fixed():
    makefile_path = os.path.join(BASE_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-g" in content, "Makefile does not contain the '-g' flag for debug symbols."
    assert "-pthread" in content or "-lpthread" in content or "pthread" in content, \
        "Makefile does not link the threading library correctly (missing -pthread)."

def test_diagnosis_report():
    diagnosis_path = "/home/user/diagnosis.txt"
    assert os.path.isfile(diagnosis_path), f"Diagnosis report not found at {diagnosis_path}"

    with open(diagnosis_path, "r") as f:
        content = f.read()

    # Parse the diagnosis file
    buggy_file_match = re.search(r"BUGGY_FILE:\s*(.*)", content)
    buggy_line_match = re.search(r"BUGGY_LINE:\s*(.*)", content)
    nan_variable_match = re.search(r"NaN_VARIABLE:\s*(.*)", content)

    assert buggy_file_match is not None, "BUGGY_FILE line is missing or malformed in diagnosis.txt"
    assert buggy_line_match is not None, "BUGGY_LINE line is missing or malformed in diagnosis.txt"
    assert nan_variable_match is not None, "NaN_VARIABLE line is missing or malformed in diagnosis.txt"

    buggy_file = buggy_file_match.group(1).strip()
    buggy_line = buggy_line_match.group(1).strip()
    nan_variable = nan_variable_match.group(1).strip()

    assert buggy_file == "pricer.cpp", f"Expected BUGGY_FILE to be 'pricer.cpp', got '{buggy_file}'"
    assert buggy_line == "21", f"Expected BUGGY_LINE to be '21', got '{buggy_line}'"
    assert nan_variable in ["out_stddev", "stddev", "var"], f"Expected NaN_VARIABLE to be 'out_stddev' (or related), got '{nan_variable}'"

def test_result_txt():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"Result file not found at {result_path}"

    with open(result_path, "r") as f:
        content = f.read().strip()

    try:
        actual_stddev = float(content)
    except ValueError:
        pytest.fail(f"result.txt does not contain a valid floating-point number. Content: '{content}'")

    data_path = os.path.join(BASE_DIR, "data.csv")
    assert os.path.isfile(data_path), f"Data file missing at {data_path}"

    data = []
    with open(data_path, "r") as f:
        for line in f:
            val = line.strip()
            if val:
                data.append(float(val))

    assert len(data) > 0, "data.csv is empty."

    # Calculate population standard deviation
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    expected_stddev = math.sqrt(variance)

    # Check if the result is within a reasonable tolerance
    assert math.isclose(actual_stddev, expected_stddev, rel_tol=1e-4), \
        f"Calculated standard deviation {actual_stddev} does not match expected {expected_stddev}."

def test_mc_pricer_compiles_and_runs():
    # Attempt to run the executable to ensure it doesn't crash and outputs the correct value
    executable_path = os.path.join(BASE_DIR, "mc_pricer")

    if not os.path.isfile(executable_path):
        # Try to build it
        subprocess.run(["make", "-C", BASE_DIR], capture_output=True)

    assert os.path.isfile(executable_path), "mc_pricer executable not found. Make sure the project builds."

    try:
        result = subprocess.run([executable_path], cwd=BASE_DIR, capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail("mc_pricer execution timed out.")

    assert result.returncode == 0, f"mc_pricer crashed or returned non-zero exit code.\nStderr: {result.stderr}"

    output = result.stdout.strip()
    try:
        actual_stddev = float(output)
    except ValueError:
        pytest.fail(f"mc_pricer output is not a valid float. Output: '{output}'")

    assert actual_stddev > 0, "Standard deviation should be positive."