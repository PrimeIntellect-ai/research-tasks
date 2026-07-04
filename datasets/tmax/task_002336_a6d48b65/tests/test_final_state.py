# test_final_state.py
import os
import subprocess
import pytest

def test_params_file():
    params_path = '/home/user/params.txt'
    assert os.path.isfile(params_path), f"File {params_path} does not exist."

    with open(params_path, 'r') as f:
        content = f.read().strip()

    parts = content.split(',')
    assert len(parts) == 3, f"Expected 3 comma-separated values in {params_path}, got {len(parts)}."

    try:
        w, mu1, mu2 = map(float, parts)
    except ValueError:
        pytest.fail(f"Could not parse parameters as floats: {content}")

    assert 0 <= w <= 1, f"Expected w to be between 0 and 1, got {w}"
    assert mu1 < mu2, f"Expected mu1 < mu2, got mu1={mu1}, mu2={mu2}"

    # Check approximate values based on truth
    assert abs(w - 0.3) < 0.1, f"w is too far from expected ~0.3, got {w}"
    assert abs(mu1 - (-2.0)) < 0.5, f"mu1 is too far from expected ~-2.0, got {mu1}"
    assert abs(mu2 - 2.0) < 0.5, f"mu2 is too far from expected ~2.0, got {mu2}"

def test_distance_file():
    dist_path = '/home/user/distance.txt'
    assert os.path.isfile(dist_path), f"File {dist_path} does not exist."

    with open(dist_path, 'r') as f:
        content = f.read().strip()

    try:
        dist = float(content)
    except ValueError:
        pytest.fail(f"Could not parse distance as float: {content}")

    assert dist < 0.1, f"Expected Wasserstein distance < 0.1, got {dist}"

def test_test_fit_script():
    script_path = '/home/user/test_fit.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"