# test_final_state.py
import os
import math

def test_results_file_exists_and_correct():
    results_path = "/home/user/results.txt"
    assert os.path.isfile(results_path), f"Results file is missing at {results_path}"

    with open(results_path, "r") as f:
        content = f.read().strip()

    assert content, "Results file is empty."

    try:
        val = float(content)
    except ValueError:
        assert False, f"Results file does not contain a valid float. Found: {content}"

    # The expected value based on the exact KDE and quad integration of the provided sequences
    # Since scipy/numpy cannot be imported in tests, we verify the expected pre-computed value.
    expected_value = 0.1702
    assert math.isclose(val, expected_value, abs_tol=0.001), f"Expected integral value close to {expected_value}, but got {val}"

def test_plot_file_exists():
    plot_path = "/home/user/plot.png"
    assert os.path.isfile(plot_path), f"Plot file is missing at {plot_path}"

    # Check if it has a valid PNG magic number
    with open(plot_path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", "The file at /home/user/plot.png is not a valid PNG image."