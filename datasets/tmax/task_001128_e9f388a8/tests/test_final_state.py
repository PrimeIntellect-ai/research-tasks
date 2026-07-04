# test_final_state.py

import os
import subprocess
import numpy as np
import pytest

def test_build_and_evaluate_mse():
    """
    Test that build.sh creates libdetector.so, and wrapper.py computes MSE
    with a Mean Absolute Error (MAE) <= 0.5 compared to NumPy.
    """
    build_script = "/home/user/build.sh"
    wrapper_script = "/home/user/wrapper.py"
    lib_path = "/home/user/libdetector.so"

    assert os.path.isfile(build_script), f"Missing {build_script}"
    assert os.access(build_script, os.X_OK), f"{build_script} is not executable. Please run chmod +x."
    assert os.path.isfile(wrapper_script), f"Missing {wrapper_script}"

    # Run build.sh to compile the shared library
    result = subprocess.run([build_script], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"build.sh failed with exit code {result.returncode}\nStderr: {result.stderr}"

    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not created by build.sh"

    np.random.seed(42)
    mae = 0.0
    num_tests = 100
    size = 230400

    tmp1 = "/tmp/test_f1.raw"
    tmp2 = "/tmp/test_f2.raw"

    for i in range(num_tests):
        f1 = np.random.randint(0, 256, size, dtype=np.uint8)
        f2 = np.random.randint(0, 256, size, dtype=np.uint8)

        with open(tmp1, "wb") as f:
            f.write(f1.tobytes())
        with open(tmp2, "wb") as f:
            f.write(f2.tobytes())

        expected_mse = np.mean((f1.astype(float) - f2.astype(float))**2)

        try:
            out = subprocess.check_output(
                ["python3", wrapper_script, tmp1, tmp2, str(size)],
                stderr=subprocess.STDOUT,
                text=True
            )
            agent_mse = float(out.strip())
        except subprocess.CalledProcessError as e:
            pytest.fail(f"wrapper.py failed on test pair {i}:\nOutput: {e.output}")
        except ValueError:
            pytest.fail(f"wrapper.py did not output a valid float on test pair {i}. Output was: '{out.strip()}'")

        mae += abs(expected_mse - agent_mse)

    mae /= num_tests

    # Cleanup
    if os.path.exists(tmp1):
        os.remove(tmp1)
    if os.path.exists(tmp2):
        os.remove(tmp2)

    assert mae <= 0.5, f"MAE {mae:.4f} exceeds threshold 0.5"