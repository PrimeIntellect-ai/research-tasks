# test_final_state.py
import os
import re

def simulate(m, dt=0.01):
    w = 0.99
    b = 2.0
    t = 0.0
    # 1000 steps for t=0 to t<10 with dt=0.01
    for _ in range(1000):
        dw = -m * w + b * w * (1 - w)
        w = w + dw * dt
    return w

def get_expected_result():
    for i in range(100, 251):
        m = i / 100.0
        w = simulate(m)
        if w < 0.1000:
            return m, w
    return None, None

def test_simulate_allele_modified():
    script_path = "/home/user/simulate_allele.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    with open(script_path, 'r') as f:
        content = f.read()
    assert "dt=0.01" in content, "simulate_allele.sh does not have dt=0.01 as default."
    assert "dt=0.5" not in content, "simulate_allele.sh still contains the old dt=0.5."

def test_optimize_m_script_exists():
    script_path = "/home/user/optimize_m.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_result_file():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    expected_m, expected_w = get_expected_result()
    assert expected_m is not None, "Could not compute expected result."

    match = re.search(r"m=([0-9.]+),\s*W=([0-9.]+)", content)
    assert match is not None, f"result.txt format is incorrect. Found: {content}"

    actual_m = float(match.group(1))
    actual_w = float(match.group(2))

    assert abs(actual_m - expected_m) < 1e-5, f"Expected m={expected_m:.2f}, got {actual_m}"
    assert abs(actual_w - expected_w) < 1e-4, f"Expected W={expected_w:.6f}, got {actual_w}"