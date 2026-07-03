# test_final_state.py
import os
import pytest

def test_posterior_mean_file():
    output_file = '/home/user/posterior_mean.txt'

    assert os.path.exists(output_file), f"Error: output file {output_file} not found."
    assert os.path.isfile(output_file), f"Error: {output_file} is not a file."

    with open(output_file, 'r') as f:
        val_str = f.read().strip()

    try:
        val = float(val_str)
    except ValueError:
        pytest.fail(f"Error: content '{val_str}' in {output_file} is not a valid float.")

    # Check if the MCMC converged near the true value (2.0)
    assert 1.7 <= val <= 2.3, f"Error: value {val} is outside acceptable range [1.7, 2.3]."

    # Check if formatted to 2 decimal places
    if '.' in val_str:
        decimals = val_str.split('.')[-1]
        assert len(decimals) == 2, f"Expected 2 decimal places, found {len(decimals)} in '{val_str}'."
    else:
        pytest.fail(f"Expected value to be formatted to 2 decimal places, but no decimal point found in '{val_str}'.")