# test_final_state.py

import os
import subprocess
import math
import pytest

def test_bad_commit_file():
    bad_commit_path = "/home/user/bad_commit.txt"
    repo_path = "/home/user/geo_service"

    assert os.path.isfile(bad_commit_path), f"File {bad_commit_path} does not exist."

    with open(bad_commit_path, "r") as f:
        commit_hash = f.read().strip()

    assert len(commit_hash) == 40, f"Expected a 40-character commit hash, got '{commit_hash}'"

    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%s", commit_hash],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        commit_msg = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to retrieve commit message for hash {commit_hash}. Git error: {e.stderr}")

    assert commit_msg == "Refactor: commit 137", f"Commit hash {commit_hash} corresponds to message '{commit_msg}', expected 'Refactor: commit 137'."

def test_calc_py_fixed():
    calc_path = "/home/user/geo_service/calc.py"
    assert os.path.isfile(calc_path), f"File {calc_path} does not exist."

    # Test with the coordinates from the pcap
    try:
        result = subprocess.run(
            ["python3", calc_path, "40.7128", "-74.006", "51.5074", "-0.1278"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running calc.py failed: {e.stderr}")

    try:
        distance = float(output)
    except ValueError:
        pytest.fail(f"calc.py output '{output}' is not a valid float.")

    expected_distance = 5570.222179737958
    assert math.isclose(distance, expected_distance, rel_tol=1e-12), \
        f"Calculated distance {distance} does not match expected {expected_distance} with high precision."

def test_calc_py_not_hardcoded():
    calc_path = "/home/user/geo_service/calc.py"

    # Test with different coordinates to ensure it's not hardcoded
    try:
        result = subprocess.run(
            ["python3", calc_path, "0", "0", "0", "0"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Running calc.py failed: {e.stderr}")

    try:
        distance = float(output)
    except ValueError:
        pytest.fail(f"calc.py output '{output}' is not a valid float.")

    assert math.isclose(distance, 0.0, abs_tol=1e-9), \
        f"Calculated distance for 0,0 to 0,0 should be 0.0, got {distance}. The solution might be hardcoded."