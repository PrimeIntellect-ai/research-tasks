# test_final_state.py

import os
import re

def test_posterior_means_file():
    txt_path = "/home/user/posterior_means.txt"
    assert os.path.isfile(txt_path), f"File not found: {txt_path}"

    with open(txt_path, "r") as f:
        content = f.read().strip()

    # Match the expected format: A: <value>, sigma_s: <value>
    match = re.search(r"A:\s*([0-9.]+),\s*sigma_s:\s*([0-9.]+)", content)
    assert match is not None, f"Content format incorrect in {txt_path}. Expected 'A: <value>, sigma_s: <value>', got: '{content}'"

    A_val = float(match.group(1))
    sigma_s_val = float(match.group(2))

    # The exact expected values with seed 42 are 5.518 and 3.205.
    # We allow a very small tolerance to account for floating point differences.
    assert abs(A_val - 5.518) <= 0.005, f"Expected A to be approximately 5.518, got {A_val}"
    assert abs(sigma_s_val - 3.205) <= 0.005, f"Expected sigma_s to be approximately 3.205, got {sigma_s_val}"

def test_mcmc_trace_png():
    png_path = "/home/user/mcmc_trace.png"
    assert os.path.isfile(png_path), f"Image file not found: {png_path}"
    assert os.path.getsize(png_path) > 0, f"Image file {png_path} is empty"