# test_final_state.py

import os

def test_mc_sampler_go_exists_and_contains_concurrency():
    """Verify that mc_sampler.go exists and uses Go concurrency primitives."""
    go_file = '/home/user/mc_sampler.go'
    assert os.path.exists(go_file), f"{go_file} does not exist."

    with open(go_file, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "go " in content, "The Go program does not appear to use goroutines ('go ' keyword missing)."

    has_chan = "chan " in content
    has_wg = "WaitGroup" in content
    assert has_chan or has_wg, "The Go program does not appear to use channels or WaitGroup for synchronization."

def test_convergence_log_exists_and_format():
    """Verify that convergence.log exists, has 3 lines, and follows the correct format."""
    log_path = '/home/user/convergence.log'
    assert os.path.exists(log_path), f"{log_path} does not exist."

    with open(log_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {log_path}, got {len(lines)}."

    try:
        n1, v1_str = lines[0].split(',')
        n2, v2_str = lines[1].split(',')
        n3, v3_str = lines[2].split(',')
    except ValueError:
        raise AssertionError("Lines in convergence.log must be formatted as 'N,value'.")

    assert n1 == "10000", f"Expected first N to be 10000, got {n1}"
    assert n2 == "100000", f"Expected second N to be 100000, got {n2}"
    assert n3 == "1000000", f"Expected third N to be 1000000, got {n3}"

    try:
        v1 = float(v1_str)
        v2 = float(v2_str)
        v3 = float(v3_str)
    except ValueError:
        raise AssertionError("The distance values in convergence.log must be valid floats.")

    assert 0.001 < v1 < 0.05, f"Value for N=10000 ({v1}) is out of expected stochastic bounds (0.001 to 0.05)."
    assert 0.0001 < v2 < 0.015, f"Value for N=100000 ({v2}) is out of expected stochastic bounds (0.0001 to 0.015)."
    assert 0.00001 < v3 < 0.005, f"Value for N=1000000 ({v3}) is out of expected stochastic bounds (0.00001 to 0.005)."

    assert v1 > v3, f"Convergence failed: distance for N=10^4 ({v1}) is not greater than N=10^6 ({v3})."