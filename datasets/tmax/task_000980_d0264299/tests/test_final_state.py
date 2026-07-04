# test_final_state.py

import os
import time
import subprocess
import pytest

def test_analyze_go_exists():
    analyze_go = "/home/user/analyze.go"
    assert os.path.isfile(analyze_go), f"analyze.go is missing: {analyze_go}"

def test_execution_time_and_success():
    analyze_go = "/home/user/analyze.go"

    start_time = time.time()
    result = subprocess.run(
        ["go", "run", analyze_go],
        capture_output=True,
        text=True,
        cwd="/home/user"
    )
    end_time = time.time()

    execution_time = end_time - start_time

    assert result.returncode == 0, f"analyze.go failed to run. Stderr: {result.stderr}"
    assert execution_time < 2.0, f"Execution time too slow: {execution_time:.2f}s (Threshold: < 2.0s). The vendor package might not be fixed."

def test_kl_divergence_output():
    kl_txt = "/home/user/kl_divergence.txt"
    assert os.path.isfile(kl_txt), f"KL divergence output missing: {kl_txt}"

    with open(kl_txt, "r") as f:
        content = f.read().strip()

    try:
        kl_val = float(content)
    except ValueError:
        pytest.fail(f"KL divergence output is not a valid float: '{content}'")

    assert kl_val >= 0.0, f"KL divergence cannot be negative, got {kl_val}"

def test_spectrum_plot_exists():
    plot_png = "/home/user/spectrum_plot.png"
    assert os.path.isfile(plot_png), f"Spectrum plot is missing: {plot_png}"
    assert os.path.getsize(plot_png) > 0, "Spectrum plot file is empty."