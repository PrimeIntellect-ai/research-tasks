# test_final_state.py

import os
import re
import subprocess
import pytest

def test_scripts_exist_and_executable():
    """Check that both scripts exist and are executable."""
    mc_volume = "/home/user/mc_volume.sh"
    convergence = "/home/user/convergence.sh"

    assert os.path.exists(mc_volume), f"{mc_volume} does not exist."
    assert os.access(mc_volume, os.X_OK), f"{mc_volume} is not executable."

    assert os.path.exists(convergence), f"{convergence} does not exist."
    assert os.access(convergence, os.X_OK), f"{convergence} is not executable."

def test_convergence_result_format_and_values():
    """Check the convergence_result.txt file for correct format and reasonable values."""
    result_file = "/home/user/convergence_result.txt"
    assert os.path.exists(result_file), f"{result_file} does not exist."

    with open(result_file, "r") as f:
        content = f.read().strip()

    match = re.match(r"^N:\s+(\d+),\s+Volume:\s+(\d+(?:\.\d+)?)$", content)
    assert match, f"Content of {result_file} does not match the expected format: 'N: <N>, Volume: <Vol>'. Got: {content}"

    n_val = int(match.group(1))
    vol_val = float(match.group(2))

    assert n_val >= 2000, f"N should be at least 2000, but got {n_val}."

    expected_vol = 33.5103
    assert abs(vol_val - expected_vol) <= 1.5, f"Estimated volume {vol_val} is too far from the expected ~33.51."

def test_mc_volume_execution():
    """Test mc_volume.sh with known parameters to ensure it calculates correctly."""
    mc_volume = "/home/user/mc_volume.sh"

    try:
        # D=4, R=1.0, N=100000, P=4
        result = subprocess.run([mc_volume, "4", "1.0", "100000", "4"], 
                                capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail("mc_volume.sh took too long to execute. It should run in parallel and return within seconds.")

    assert result.returncode == 0, f"mc_volume.sh failed with error: {result.stderr}"

    output = result.stdout.strip()
    try:
        vol = float(output)
    except ValueError:
        pytest.fail(f"mc_volume.sh output is not a valid float: '{output}'")

    # True volume of 4D hypersphere with R=1 is pi^2 / 2 ≈ 4.9348
    expected_vol = 4.9348
    assert abs(vol - expected_vol) <= 0.5, f"mc_volume.sh returned {vol}, expected roughly {expected_vol}."