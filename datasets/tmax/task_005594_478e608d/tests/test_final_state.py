# test_final_state.py
import os
import subprocess
import sys

def test_output_files_exist():
    """Verify that the required output files exist."""
    output_h5 = "/home/user/output_states.h5"
    output_txt = "/home/user/avg_x.txt"

    assert os.path.isfile(output_h5), f"Missing required output file: {output_h5}"
    assert os.path.isfile(output_txt), f"Missing required output file: {output_txt}"

def test_correctness_via_subprocess():
    """
    Verify the contents of the HDF5 file and the text file by computing the expected
    truth using scipy/numpy/h5py in a subprocess. This avoids importing third-party
    libraries directly in the pytest environment.
    """
    script = """
import sys
try:
    import numpy as np
    import h5py
    from scipy.integrate import solve_ivp
except ImportError as e:
    print(f"Missing required library: {e}")
    sys.exit(1)

# 1. Read input states
try:
    with h5py.File('/home/user/input_states.h5', 'r') as f:
        states = f['states'][:]
except Exception as e:
    print(f"Failed to read input_states.h5: {e}")
    sys.exit(1)

# 2. Compute expected final states
def dSdt(t, S):
    x, v = S
    return [v, -x**3]

expected_final_states = []
for S0 in states:
    sol = solve_ivp(dSdt, [0, 5.0], S0, method='RK45')
    expected_final_states.append([sol.y[0, -1], sol.y[1, -1]])

expected_final_states = np.array(expected_final_states)
expected_avg_x = np.mean(expected_final_states[:, 0])
expected_avg_x_str = f"{expected_avg_x:.4f}"

# 3. Read output states
try:
    with h5py.File('/home/user/output_states.h5', 'r') as f:
        if 'final_states' not in f:
            print("Dataset '/final_states' not found in output_states.h5")
            sys.exit(1)
        out_states = f['final_states'][:]
        out_dtype = f['final_states'].dtype
except Exception as e:
    print(f"Failed to read output_states.h5: {e}")
    sys.exit(1)

# 4. Verify output states
if out_states.shape != (1000, 2):
    print(f"Expected shape (1000, 2), got {out_states.shape}")
    sys.exit(1)

if out_dtype != np.float64:
    print(f"Expected dtype float64, got {out_dtype}")
    sys.exit(1)

if not np.allclose(expected_final_states, out_states, atol=1e-3):
    print("The integrated final states in output_states.h5 do not match the expected values.")
    sys.exit(1)

# 5. Verify avg_x.txt
try:
    with open('/home/user/avg_x.txt', 'r') as f:
        avg_x_content = f.read().strip()
except Exception as e:
    print(f"Failed to read avg_x.txt: {e}")
    sys.exit(1)

if avg_x_content != expected_avg_x_str:
    print(f"Average x mismatch: expected '{expected_avg_x_str}', got '{avg_x_content}'")
    sys.exit(1)

print("SUCCESS")
"""
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True)
    assert result.returncode == 0, f"Verification failed!\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    assert "SUCCESS" in result.stdout, "Verification script did not complete successfully."