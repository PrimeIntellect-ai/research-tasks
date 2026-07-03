# test_final_state.py

import os
import pytest

def test_trace_csv_exists():
    """Test that the simulator was run and produced trace.csv."""
    trace_file = "/home/user/trace.csv"
    assert os.path.isfile(trace_file), f"File {trace_file} is missing. Did you compile and run sim.rs?"
    assert os.path.getsize(trace_file) > 0, f"File {trace_file} is empty."

def test_analyze_rs_exists():
    """Test that the analysis script was created."""
    analyze_file = "/home/user/analyze.rs"
    assert os.path.isfile(analyze_file), f"File {analyze_file} is missing. Did you write the analysis program?"
    assert os.path.getsize(analyze_file) > 0, f"File {analyze_file} is empty."

def test_k_estimate_correct():
    """Test that the estimated k is correct and saved properly."""
    k_file = "/home/user/k_estimate.txt"
    assert os.path.isfile(k_file), f"File {k_file} is missing. Did you save the estimate?"

    with open(k_file, "r") as f:
        content = f.read().strip()

    assert content == "0.8", f"Expected k estimate to be '0.8', but got '{content}'."