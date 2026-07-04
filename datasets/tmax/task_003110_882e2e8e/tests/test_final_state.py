# test_final_state.py
import os
import pytest

def test_final_mse_value():
    """Check that the final MSE is computed correctly without data leakage."""
    mse_file = '/home/user/final_mse.txt'
    assert os.path.isfile(mse_file), f"File {mse_file} does not exist. Did you save the final MSE?"

    with open(mse_file, 'r') as f:
        content = f.read().strip()

    try:
        agent_mse = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {mse_file} as a float. Found: '{content}'")

    # Reference value calculated by correctly splitting 300 frames, computing 
    # training stats, and validating on the holdout fold.
    REFERENCE_MSE = 1.4523  
    TOLERANCE = 0.05

    diff = abs(agent_mse - REFERENCE_MSE)
    assert diff <= TOLERANCE, (
        f"Failure: Agent MSE {agent_mse} is not within {TOLERANCE} of "
        f"reference MSE {REFERENCE_MSE}. Difference is {diff:.4f}. "
        "Make sure the data leak is fully fixed (mean/std computed only on train folds)."
    )