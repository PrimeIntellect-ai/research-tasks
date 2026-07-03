# test_final_state.py

import os
import re

def test_output_plot_exists_and_valid():
    """Check that the plot was generated and is a valid PNG file."""
    path = "/home/user/output_plot.png"
    assert os.path.isfile(path), f"Output plot not found: {path}"

    with open(path, "rb") as f:
        header = f.read(8)
    # Check PNG magic bytes
    assert header == b"\x89PNG\r\n\x1a\n", "output_plot.png is not a valid PNG file"

def test_metrics_txt_content():
    """Check that metrics.txt was generated with the correct computed values."""
    path = "/home/user/metrics.txt"
    assert os.path.isfile(path), f"Metrics file not found: {path}"

    with open(path, "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) == 3, f"metrics.txt must have exactly 3 lines, found {len(content)}"

    # The expected values are deterministic based on the provided seeds and data.
    # Since numpy's specific PRNG and percentile algorithms cannot be perfectly 
    # replicated in pure Python stdlib, we assert against the known expected outputs.
    expected_mean = "Mean: 101.44"
    expected_ci = "CI: 98.66-104.29"
    expected_pred = "Prediction: 1.50"

    assert content[0].strip() == expected_mean, f"Line 1 mismatch. Expected '{expected_mean}', got '{content[0].strip()}'"
    assert content[1].strip() == expected_ci, f"Line 2 mismatch. Expected '{expected_ci}', got '{content[1].strip()}'"
    assert content[2].strip() == expected_pred, f"Line 3 mismatch. Expected '{expected_pred}', got '{content[2].strip()}'"