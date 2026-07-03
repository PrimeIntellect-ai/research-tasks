# test_final_state.py
import os
import json
import math

def test_svd_top3():
    user_file = '/home/user/svd_top3.txt'
    truth_file = '/tmp/truth_svd.txt'

    assert os.path.exists(user_file), f"File {user_file} does not exist. The task requires saving the top 3 singular values here."
    assert os.path.exists(truth_file), f"Truth file {truth_file} does not exist."

    with open(user_file, 'r') as f:
        user_content = f.read().strip()
    with open(truth_file, 'r') as f:
        truth_content = f.read().strip()

    user_vals = [v.strip() for v in user_content.split(',')]
    truth_vals = [v.strip() for v in truth_content.split(',')]

    assert len(user_vals) == 3, f"Expected exactly 3 comma-separated values in {user_file}, but found {len(user_vals)}."

    for i, (u, t) in enumerate(zip(user_vals, truth_vals)):
        try:
            u_float = float(u)
            t_float = float(t)
        except ValueError:
            assert False, f"Value '{u}' in {user_file} is not a valid float."

        assert math.isclose(u_float, t_float, abs_tol=1e-3), f"Singular value {i+1} mismatch: expected {t_float}, got {u_float}"

def test_kinetics():
    user_file = '/home/user/kinetics.json'
    truth_file = '/tmp/truth_kinetics.json'

    assert os.path.exists(user_file), f"File {user_file} does not exist. The task requires saving the fitted parameters here."
    assert os.path.exists(truth_file), f"Truth file {truth_file} does not exist."

    with open(user_file, 'r') as f:
        try:
            user_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {user_file} does not contain valid JSON."

    with open(truth_file, 'r') as f:
        truth_data = json.load(f)

    for key in ['k1', 'k2']:
        assert key in user_data, f"Key '{key}' is missing from {user_file}."
        u_val = user_data[key]
        t_val = truth_data[key]

        assert isinstance(u_val, (int, float)), f"Value for '{key}' in {user_file} must be a number."
        assert math.isclose(u_val, t_val, abs_tol=0.0005), f"Value for '{key}' mismatch: expected {t_val}, got {u_val}"