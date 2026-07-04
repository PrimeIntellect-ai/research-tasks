# test_final_state.py

import os
import math

def test_correlation_file_content():
    corr_file = "/home/user/correlation.txt"
    assert os.path.isfile(corr_file), f"Correlation file {corr_file} is missing."

    with open(corr_file, "r") as f:
        content = f.read().strip()

    # The expected correlation is 0.9859 based on the deterministic data generation
    # X = [1.0, 2.0, ..., 50.0]
    # Y = [0.5 * X_i + (X_i % 4)]
    expected_corr = "0.9859"

    assert content == expected_corr, f"Expected correlation value '{expected_corr}', but got '{content}'."

def test_scatter_plot_exists_and_size():
    scatter_file = "/home/user/scatter.png"
    assert os.path.isfile(scatter_file), f"Scatter plot file {scatter_file} is missing."

    size = os.path.getsize(scatter_file)
    assert size > 100, f"Scatter plot file {scatter_file} is too small ({size} bytes), likely blank or invalid."

def test_scatter_plot_is_png():
    scatter_file = "/home/user/scatter.png"
    assert os.path.isfile(scatter_file), f"Scatter plot file {scatter_file} is missing."

    with open(scatter_file, "rb") as f:
        header = f.read(8)

    # PNG magic number: \x89PNG\r\n\x1a\n
    expected_magic = b"\x89PNG\r\n\x1a\n"
    assert header == expected_magic, f"Scatter plot file {scatter_file} is not a valid PNG image based on its magic bytes."