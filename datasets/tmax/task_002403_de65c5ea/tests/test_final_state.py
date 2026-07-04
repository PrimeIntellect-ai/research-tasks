# test_final_state.py
import os
import re
import pytest

def test_c_source_exists():
    c_file = "/home/user/bootstrap_regression.c"
    assert os.path.exists(c_file), f"C source file {c_file} does not exist."
    assert os.path.isfile(c_file), f"Path {c_file} is not a file."

def test_regression_results_exists_and_format():
    results_file = "/home/user/regression_results.txt"
    assert os.path.exists(results_file), f"Output file {results_file} does not exist."
    assert os.path.isfile(results_file), f"Path {results_file} is not a file."

    with open(results_file, "r") as f:
        content = f.read().strip()

    # Format: Slope: [original_slope], 95% CI: [[lower_bound], [upper_bound]]
    # Example: Slope: 211.75, 95% CI: [175.76, 256.36]
    pattern = r"^Slope:\s*([0-9\.-]+),\s*95%\s*CI:\s*\[([0-9\.-]+),\s*([0-9\.-]+)\]$"
    match = re.match(pattern, content)
    assert match is not None, f"Content of {results_file} does not match the expected format: 'Slope: X.XX, 95% CI: [Y.YY, Z.ZZ]'. Found: {content}"

    slope_str, lower_str, upper_str = match.groups()
    try:
        slope = float(slope_str)
        lower = float(lower_str)
        upper = float(upper_str)
    except ValueError:
        pytest.fail("Parsed values for slope or CI bounds are not valid floats.")

    # Original slope should be ~211.75
    assert abs(slope - 211.75) < 0.1, f"Expected original slope around 211.75, but got {slope}."

    # Lower bound should be between 170 and 180
    assert 170.0 <= lower <= 180.0, f"Expected lower bound between 170 and 180, but got {lower}."

    # Upper bound should be between 250 and 265
    assert 250.0 <= upper <= 265.0, f"Expected upper bound between 250 and 265, but got {upper}."