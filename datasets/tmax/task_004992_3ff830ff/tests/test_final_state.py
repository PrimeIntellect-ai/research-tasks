# test_final_state.py
import os
import re
import pytest

def test_binary_exists():
    binary_path = "/home/user/mutator/target/release/mutator"
    assert os.path.isfile(binary_path), f"The compiled Rust binary was not found at {binary_path}. Did you run 'cargo build --release'?"

def test_summary_file_exists():
    summary_path = "/home/user/results/summary.txt"
    assert os.path.isfile(summary_path), f"The summary file was not found at {summary_path}. Did you execute the Jupyter notebook?"

def test_summary_content_and_p_value():
    summary_path = "/home/user/results/summary.txt"
    with open(summary_path, "r") as f:
        content = f.read().strip()

    assert "Workflow Complete" in content, "The summary text does not contain 'Workflow Complete'."
    assert "p_value:" in content, "The summary text does not contain 'p_value:'."

    # Extract the p-value
    match = re.search(r"p_value:\s*([0-9.]+)", content)
    assert match is not None, "Could not parse a numeric p_value from summary.txt."

    try:
        p_val = float(match.group(1))
    except ValueError:
        pytest.fail(f"Parsed p_value '{match.group(1)}' is not a valid float.")

    # If the RNG is still inside the loop, the p_value will be exactly 1.0 or 0.0.
    # A correct Monte Carlo simulation will yield a fractional value (around 0.78).
    assert p_val != 1.0, "p_value is exactly 1.0. The RNG or file reading is likely still inside the loop."
    assert p_val != 0.0, "p_value is exactly 0.0. The RNG or file reading is likely still inside the loop."
    assert 0.0 < p_val < 1.0, f"p_value {p_val} is out of expected statistical bounds."