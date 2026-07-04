# test_final_state.py

import json
import numpy as np
import os

def test_estimates_json():
    """Evaluate the estimated parameters by computing the MSE of the frequency curve."""
    filepath = '/home/user/estimates.json'
    assert os.path.exists(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {filepath} is not valid JSON."

    assert 'alpha' in data, "Missing 'alpha' in estimates.json"
    assert 'beta' in data, "Missing 'beta' in estimates.json"
    assert 'gamma' in data, "Missing 'gamma' in estimates.json"

    try:
        a_est = float(data['alpha'])
        b_est = float(data['beta'])
        c_est = float(data['gamma'])
    except ValueError:
        assert False, "Values in estimates.json must be numeric."

    t = np.linspace(0, 1, 100)
    f_true = 500.0 * np.exp(2.0 * t) + 300.0
    f_est = a_est * np.exp(b_est * t) + c_est

    mse = np.mean((f_true - f_est)**2)

    assert mse <= 2500.0, f"MSE {mse:.2f} is greater than the threshold 2500.0"