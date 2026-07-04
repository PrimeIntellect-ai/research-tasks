# test_final_state.py

import os
import re

def test_files_exist():
    """Verify that all required files exist."""
    expected_files = [
        "/home/user/data_prep.cpp",
        "/home/user/samples.csv",
        "/home/user/results.txt",
        "/home/user/plot_samples.py",
        "/home/user/histogram.png"
    ]
    for filepath in expected_files:
        assert os.path.exists(filepath), f"Required file missing: {filepath}"

def test_results_txt_content():
    """Verify the contents and calculated variances in results.txt."""
    results_path = "/home/user/results.txt"
    with open(results_path, 'r') as f:
        text = f.read()

    exact_match = re.search(r"Exact:\s*([0-9.]+)", text)
    mcmc_match = re.search(r"MCMC:\s*([0-9.]+)", text)

    assert exact_match, "Could not parse 'Exact:' value from results.txt"
    assert mcmc_match, "Could not parse 'MCMC:' value from results.txt"

    exact_val = float(exact_match.group(1))
    mcmc_val = float(mcmc_match.group(1))

    assert 1.000 <= exact_val <= 1.004, f"Exact variance {exact_val} is outside expected bounds [1.000, 1.004]"
    assert 0.95 <= mcmc_val <= 1.05, f"MCMC variance {mcmc_val} is outside expected bounds [0.95, 1.05]"

def test_samples_csv_length():
    """Verify that samples.csv contains exactly 90,000 lines."""
    samples_path = "/home/user/samples.csv"
    with open(samples_path, 'r') as f:
        lines = f.readlines()

    # Allow for empty lines at the end
    non_empty_lines = [line for line in lines if line.strip()]
    assert len(non_empty_lines) == 90000, f"Expected 90,000 lines in samples.csv, got {len(non_empty_lines)}"

def test_histogram_png_valid():
    """Verify that histogram.png is generated and is not empty."""
    image_path = "/home/user/histogram.png"
    assert os.path.getsize(image_path) > 0, "histogram.png exists but is empty"