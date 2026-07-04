# test_final_state.py

import os
import ctypes
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/sys_debug"

def test_libraries_built():
    """Test if libmatrix.so and libgraph.so have been built."""
    assert os.path.isfile(os.path.join(WORKSPACE_DIR, "libmatrix.so")), "libmatrix.so is missing. Did you run make?"
    assert os.path.isfile(os.path.join(WORKSPACE_DIR, "libgraph.so")), "libgraph.so is missing. Did you run make?"

def test_libgraph_linking():
    """Test if libgraph.so correctly links against libmatrix.so and can be loaded."""
    # Temporarily add WORKSPACE_DIR to LD_LIBRARY_PATH to allow ctypes to resolve libmatrix.so
    # if it was linked with -L. -lmatrix
    env = os.environ.copy()
    ld_lib_path = env.get("LD_LIBRARY_PATH", "")
    env["LD_LIBRARY_PATH"] = f"{WORKSPACE_DIR}:{ld_lib_path}"

    try:
        # Run a small python script in a subprocess with the modified environment
        # to see if it can load libgraph.so successfully.
        script = f"""
import ctypes
try:
    ctypes.CDLL('{WORKSPACE_DIR}/libgraph.so')
except Exception as e:
    import sys
    sys.exit(1)
"""
        result = subprocess.run(["python3", "-c", script], env=env, capture_output=True, text=True)
        assert result.returncode == 0, f"Failed to load libgraph.so via ctypes. It might not be correctly linked against libmatrix.so. Error: {result.stderr}"
    except Exception as e:
        pytest.fail(f"Exception during loading test: {e}")

def test_solver_script_exists():
    """Test if the solver.py script was created."""
    solver_path = os.path.join(WORKSPACE_DIR, "solver.py")
    assert os.path.isfile(solver_path), f"{solver_path} does not exist."

def test_output_log():
    """Test if output.log exists and contains the correct traversal count."""
    log_path = os.path.join(WORKSPACE_DIR, "output.log")
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did solver.py run successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "7", f"Expected output.log to contain '7', but got '{content}'."