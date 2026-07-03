# test_final_state.py

import os
import re
import pytest

def test_posterior_txt_exists():
    """Test that the posterior.txt file exists."""
    file_path = "/home/user/posterior.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you create it?"

def test_posterior_values():
    """Test that the posterior.txt contains correct m and c values."""
    file_path = "/home/user/posterior.txt"
    with open(file_path, 'r') as f:
        content = f.read().strip()

    # Expecting format: m=<value>,c=<value>
    match = re.match(r'^m=([0-9\.\-]+),c=([0-9\.\-]+)$', content)
    assert match is not None, f"Content of {file_path} is not in the expected format 'm=<value>,c=<value>'. Found: {content}"

    m_val = float(match.group(1))
    c_val = float(match.group(2))

    # Check if they are close to the true values (m~3.1415, c~2.7182)
    assert 3.10 <= m_val <= 3.20, f"Value of m ({m_val}) is not within the expected range. Did Kahan summation fix the precision issue?"
    assert 2.65 <= c_val <= 2.80, f"Value of c ({c_val}) is not within the expected range. Did Kahan summation fix the precision issue?"

def test_mcmc_fit_c_kahan_implementation():
    """Test that mcmc_fit.c has been modified to include Kahan summation logic."""
    file_path = "/home/user/mcmc_fit.c"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read()

    # A basic check to ensure the compute_sse function signature wasn't changed
    assert "float compute_sse(float* x, float* y, int n, float m, float c)" in content, \
        "The compute_sse function signature was changed. It must remain the same."

    # Check for variables/operations indicative of Kahan summation
    # Kahan summation typically involves a compensation variable (c or err) and subtracting it
    # We will just look for multiple additions/subtractions in the loop
    # The naive loop had `sum += err * err;`
    # We expect something more complex now.
    lines = content.split('\n')
    in_compute_sse = False
    loop_lines = []
    for line in lines:
        if "float compute_sse" in line:
            in_compute_sse = True
        if in_compute_sse:
            loop_lines.append(line)
            if "return" in line:
                break

    compute_sse_body = "\n".join(loop_lines)

    # Check if there's an assignment that looks like Kahan compensation
    # We won't be overly strict on variable names, but we expect more than just sum += err * err
    # Kahan has at least 3 assignments to update the sum and compensation.
    assignments = compute_sse_body.count('=')
    assert assignments >= 5, "compute_sse does not seem to contain the Kahan summation algorithm (not enough operations)."