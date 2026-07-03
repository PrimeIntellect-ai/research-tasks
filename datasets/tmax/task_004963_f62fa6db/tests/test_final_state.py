# test_final_state.py

import os
import math
import subprocess
import pytest

def test_result_file_exists_and_correct():
    path = "/home/user/result.txt"
    assert os.path.isfile(path), f"File {path} is missing. Did you run the script and redirect output?"

    with open(path, 'r') as f:
        content = f.read().strip()

    assert "StdDev:" in content, f"Output in {path} does not contain 'StdDev:'"

    # Extract the number
    try:
        val_str = content.split("StdDev:")[1].strip()
        val = float(val_str)
    except Exception as e:
        pytest.fail(f"Could not parse standard deviation from {path}: {e}")

    # The expected population stddev for [-1000000000, -1000000001, -1000000002]
    # Variance is 2/3, stddev is sqrt(2/3) ~ 0.81649658
    expected = math.sqrt(2.0 / 3.0)
    assert math.isclose(val, expected, rel_tol=1e-4), f"Expected StdDev close to {expected:.6f}, got {val}"

def test_fuzzing_passes():
    fuzz_script = "/home/user/fuzz.sh"
    assert os.path.isfile(fuzz_script), f"Fuzz script {fuzz_script} missing."

    # Run the fuzz script to ensure the numerical instability bug is fixed
    result = subprocess.run(["bash", fuzz_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Fuzz test failed, indicating numerical instability is still present:\n{result.stdout}\n{result.stderr}"