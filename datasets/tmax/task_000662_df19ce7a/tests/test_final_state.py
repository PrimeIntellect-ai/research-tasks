# test_final_state.py

import os
import re
import math
import subprocess
import pytest

def test_bootstrap_cpp_exists_and_contains_openmp():
    cpp_path = "/home/user/bootstrap.cpp"
    assert os.path.isfile(cpp_path), f"Missing file: {cpp_path}"

    with open(cpp_path, "r") as f:
        content = f.read()

    assert "#pragma omp parallel for" in content, "bootstrap.cpp does not contain OpenMP pragma '#pragma omp parallel for'."

def test_run_analysis_sh_exists_and_valid():
    sh_path = "/home/user/run_analysis.sh"
    assert os.path.isfile(sh_path), f"Missing file: {sh_path}"

    with open(sh_path, "r") as f:
        content = f.read()

    assert "-fopenmp" in content, "run_analysis.sh does not compile with -fopenmp."
    assert "g++" in content, "run_analysis.sh does not use g++ to compile."

def test_run_analysis_and_check_ci():
    sh_path = "/home/user/run_analysis.sh"
    ci_path = "/home/user/ci.txt"

    # Run the bash script
    result = subprocess.run(["bash", sh_path], capture_output=True, text=True)
    assert result.returncode == 0, f"run_analysis.sh failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(ci_path), f"run_analysis.sh did not create {ci_path}."

    # Compute the expected CI in Python
    data_path = "/home/user/data.txt"
    indices_path = "/home/user/indices.txt"

    with open(data_path, "r") as f:
        data = [float(line.strip()) for line in f if line.strip()]

    means = []
    with open(indices_path, "r") as f:
        for line in f:
            if not line.strip():
                continue
            indices = [int(x) for x in line.strip().split()]
            mean = sum(data[i] for i in indices) / len(indices)
            means.append(mean)

    means.sort()
    expected_lower = means[249]
    expected_upper = means[9749]

    # Read the generated ci.txt
    with open(ci_path, "r") as f:
        ci_content = f.read()

    lower_match = re.search(r"Lower CI:\s*([0-9.]+)", ci_content)
    upper_match = re.search(r"Upper CI:\s*([0-9.]+)", ci_content)

    assert lower_match, "Could not parse 'Lower CI: <value>' from ci.txt"
    assert upper_match, "Could not parse 'Upper CI: <value>' from ci.txt"

    actual_lower = float(lower_match.group(1))
    actual_upper = float(upper_match.group(1))

    # Check if values are close (allow small floating point differences)
    assert math.isclose(actual_lower, expected_lower, rel_tol=1e-4), f"Lower CI mismatch. Expected ~{expected_lower}, got {actual_lower}"
    assert math.isclose(actual_upper, expected_upper, rel_tol=1e-4), f"Upper CI mismatch. Expected ~{expected_upper}, got {actual_upper}"