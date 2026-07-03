# test_final_state.py
import os
import numpy as np

def test_final_series_mse():
    target_path = '/home/user/diffusion_sim/output/final_series.npy'
    truth_path = '/app/hidden_truth.npy'

    assert os.path.isfile(target_path), f"Agent output file missing at {target_path}"
    assert os.path.isfile(truth_path), f"Truth file missing at {truth_path}"

    try:
        agent_arr = np.load(target_path)
    except Exception as e:
        assert False, f"Failed to load agent output array from {target_path}: {e}"

    try:
        true_arr = np.load(truth_path)
    except Exception as e:
        assert False, f"Failed to load truth array from {truth_path}: {e}"

    assert agent_arr.shape == true_arr.shape, (
        f"Shape mismatch: agent array has shape {agent_arr.shape}, but truth has shape {true_arr.shape}. "
        "Did you drop the corrupted rows correctly?"
    )

    mse = np.mean((agent_arr - true_arr)**2)
    threshold = 1e-4

    assert mse <= threshold, (
        f"Output data does not match expected values closely enough.\n"
        f"Measured MSE: {mse}\n"
        f"Threshold: {threshold}\n"
        f"Check that you used the correct kappa and tau values from the image, "
        f"and implemented the correct numerical stability fix in math_core.py."
    )