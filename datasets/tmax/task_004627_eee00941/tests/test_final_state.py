# test_final_state.py

import os
import subprocess
import numpy as np
import pytest

def test_reconstructed_model_exists():
    model_path = "/home/user/reconstructed_model.py"
    assert os.path.exists(model_path), f"Missing reconstructed model script: {model_path}"
    assert os.path.isfile(model_path), f"Path is not a file: {model_path}"

def test_reconstructed_model_mse():
    model_path = "/home/user/reconstructed_model.py"
    binary_path = "/app/sensor_encoder"

    assert os.path.exists(model_path), f"Missing reconstructed model script: {model_path}"
    assert os.path.exists(binary_path), f"Missing legacy tool binary: {binary_path}"

    np.random.seed(42)
    # Generate 1000 random inputs of 10 floats
    num_tests = 1000
    test_inputs = np.random.randn(num_tests, 10).astype(np.float32)

    y_true = []
    y_pred = []

    for i in range(num_tests):
        inp = test_inputs[i]
        str_args = [str(x) for x in inp]

        # Run true binary
        try:
            res_true = subprocess.run([binary_path] + str_args, capture_output=True, text=True, check=True)
            out_true = np.array([float(x) for x in res_true.stdout.strip().split()])
            y_true.append(out_true)
        except Exception as e:
            pytest.fail(f"Failed to run legacy binary on input {inp}: {e}")

        # Run predicted script
        try:
            res_pred = subprocess.run(["python3", model_path] + str_args, capture_output=True, text=True, check=True)
            out_pred = np.array([float(x) for x in res_pred.stdout.strip().split()])
            y_pred.append(out_pred)
        except Exception as e:
            pytest.fail(f"Failed to run reconstructed model on input {inp}: {e}\nStdout: {res_pred.stdout if 'res_pred' in locals() else ''}\nStderr: {res_pred.stderr if 'res_pred' in locals() else ''}")

    y_true = np.array(y_true)
    y_pred = np.array(y_pred)

    mse = np.mean((y_true - y_pred) ** 2)
    threshold = 1e-10

    assert mse <= threshold, f"MSE {mse} exceeds threshold {threshold}. Reconstructed model does not match legacy binary."