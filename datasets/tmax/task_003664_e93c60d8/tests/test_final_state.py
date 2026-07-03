# test_final_state.py
import os
import subprocess
import numpy as np
import tempfile

def test_predictor_exists():
    path = "/home/user/predictor"
    assert os.path.exists(path), f"Missing predictor executable at {path}"
    assert os.path.isfile(path), f"{path} is not a file"
    assert os.access(path, os.X_OK), f"{path} is not executable"

def test_cv_results_log_exists():
    path = "/home/user/cv_results.log"
    assert os.path.exists(path), f"Missing cv_results.log at {path}"
    assert os.path.isfile(path), f"{path} is not a file"

def test_predictor_mse():
    np.random.seed(42)
    # Generate 10,000 random rows with values between -10 and 10
    X = np.random.uniform(-10, 10, size=(10000, 5))

    with tempfile.TemporaryDirectory() as tmpdir:
        test_csv = os.path.join(tmpdir, "hidden_test.csv")
        np.savetxt(test_csv, X, delimiter=",", fmt="%.6f")

        oracle_out = os.path.join(tmpdir, "oracle_out.txt")
        predictor_out = os.path.join(tmpdir, "predictor_out.txt")

        # Run oracle
        try:
            with open(oracle_out, "w") as f:
                subprocess.run(["/app/oracle", test_csv], stdout=f, check=True)
        except subprocess.CalledProcessError as e:
            assert False, f"Oracle failed to run: {e}"

        # Run predictor
        try:
            with open(predictor_out, "w") as f:
                subprocess.run(["/home/user/predictor", test_csv], stdout=f, check=True, timeout=30)
        except subprocess.CalledProcessError as e:
            assert False, f"Predictor failed to run: {e}"
        except subprocess.TimeoutExpired as e:
            assert False, f"Predictor timed out: {e}"

        # Read outputs
        try:
            oracle_vals = np.loadtxt(oracle_out)
        except Exception as e:
            assert False, f"Failed to read oracle output: {e}"

        try:
            pred_vals = np.loadtxt(predictor_out)
        except Exception as e:
            assert False, f"Failed to read predictor output. Ensure it prints one float per line. Error: {e}"

        assert len(oracle_vals) == len(X), "Oracle output length mismatch"
        assert len(pred_vals) == len(X), f"Predictor output length mismatch: expected {len(X)}, got {len(pred_vals)}"

        # Compute MSE
        mse = np.mean((oracle_vals - pred_vals)**2)
        assert mse < 0.01, f"MSE is too high: {mse:.6f} >= 0.01. The model did not accurately approximate the oracle."