# test_final_state.py
import os
import subprocess
import pytest

def test_best_k():
    best_k_path = "/home/user/best_k.txt"
    assert os.path.isfile(best_k_path), f"{best_k_path} is missing"

    with open(best_k_path, "r") as f:
        content = f.read().strip()

    try:
        k = float(content)
    except ValueError:
        pytest.fail(f"Could not parse '{content}' as a float in {best_k_path}")

    assert abs(k - 0.5) < 0.01, f"Expected k to be ~0.5, got {k}"

def test_fit_script_exists_and_executable():
    fit_path = "/home/user/fit.sh"
    assert os.path.isfile(fit_path), f"{fit_path} is missing"
    assert os.access(fit_path, os.X_OK), f"{fit_path} is not executable"

def ks_2samp_stdlib(data1, data2):
    n1 = len(data1)
    n2 = len(data2)
    data1 = sorted(data1)
    data2 = sorted(data2)
    data_all = sorted(set(data1 + data2))

    max_d = 0.0
    i1 = 0
    i2 = 0

    for x in data_all:
        while i1 < n1 and data1[i1] <= x:
            i1 += 1
        while i2 < n2 and data2[i2] <= x:
            i2 += 1

        cdf1 = i1 / n1
        cdf2 = i2 / n2
        max_d = max(max_d, abs(cdf1 - cdf2))

    return max_d

def test_ks_dist():
    ks_path = "/home/user/ks_dist.txt"
    assert os.path.isfile(ks_path), f"{ks_path} is missing"

    with open(ks_path, "r") as f:
        content = f.read().strip()

    try:
        ks_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse '{content}' as a float in {ks_path}")

    # Recompute expected KS distance based on the student's simulate.py
    obs_path = "/home/user/observed.txt"
    assert os.path.isfile(obs_path), f"{obs_path} is missing"

    obs_y = []
    with open(obs_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                obs_y.append(float(parts[1]))

    # Run simulate.py with k=0.5
    sim_path = "/home/user/simulate.py"
    result = subprocess.run(["python3", sim_path, "0.5"], capture_output=True, text=True)
    assert result.returncode == 0, f"simulate.py failed with k=0.5. stderr: {result.stderr}"

    sim_y = []
    for line in result.stdout.strip().split("\n"):
        parts = line.strip().split()
        if len(parts) >= 2:
            sim_y.append(float(parts[1]))

    assert len(sim_y) == 11, f"simulate.py should output exactly 11 points, got {len(sim_y)}"
    assert len(obs_y) == 11, f"observed.txt should have exactly 11 points, got {len(obs_y)}"

    expected_ks = ks_2samp_stdlib(obs_y, sim_y)

    assert abs(ks_val - expected_ks) < 0.015, f"Expected KS distance ~{expected_ks:.3f}, got {ks_val}"