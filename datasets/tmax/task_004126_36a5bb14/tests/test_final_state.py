# test_final_state.py

import os
import pytest

def test_analyze_sim_script_exists():
    """
    Test that the analysis script exists.
    """
    script_file = "/home/user/analyze_sim.py"
    assert os.path.isfile(script_file), f"The script {script_file} does not exist."

def test_distributions_png_exists():
    """
    Test that the distributions plot exists and is a valid PNG file.
    """
    png_path = "/home/user/distributions.png"
    assert os.path.isfile(png_path), f"The plot {png_path} does not exist."

    with open(png_path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", f"The file {png_path} is not a valid PNG image."

def test_wasserstein_txt():
    """
    Test that the wasserstein distance output is correct.
    """
    single_path = "/home/user/single_thread.csv"
    multi_path = "/home/user/multi_thread.csv"
    txt_path = "/home/user/wasserstein.txt"

    assert os.path.isfile(single_path), f"Missing input file: {single_path}"
    assert os.path.isfile(multi_path), f"Missing input file: {multi_path}"
    assert os.path.isfile(txt_path), f"Missing output file: {txt_path}"

    # Read the data
    with open(single_path, "r") as f:
        single = [float(line.strip()) for line in f if line.strip()]
    with open(multi_path, "r") as f:
        multi = [float(line.strip()) for line in f if line.strip()]

    assert len(single) == len(multi), "Data files have different number of lines."
    assert len(single) > 0, "Data files are empty."

    # Compute 1D Wasserstein distance for uniformly weighted samples of the same size
    # This is exactly the mean absolute difference of the sorted arrays
    single.sort()
    multi.sort()
    dist = sum(abs(s - m) for s, m in zip(single, multi)) / len(single)
    expected_str = f"{dist:.4f}"

    with open(txt_path, "r") as f:
        actual_str = f.read().strip()

    assert actual_str == expected_str, (
        f"Incorrect Wasserstein distance in {txt_path}. "
        f"Expected: '{expected_str}', Found: '{actual_str}'"
    )