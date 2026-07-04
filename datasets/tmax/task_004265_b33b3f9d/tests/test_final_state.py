# test_final_state.py
import os
import subprocess
import stat

def test_worker_fixed_exists_and_executable():
    path = "/home/user/worker_fixed.sh"
    assert os.path.isfile(path), f"The file {path} should exist."
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"The file {path} should be executable."

def test_worker_fixed_does_not_hang():
    path = "/home/user/worker_fixed.sh"
    try:
        # Run the fixed script with input 1.0, which previously caused an infinite loop
        result = subprocess.run([path, "1.0"], capture_output=True, timeout=3, text=True)
        assert result.returncode == 0, f"{path} failed with return code {result.returncode}. stderr: {result.stderr}"
    except subprocess.TimeoutExpired:
        assert False, f"{path} hung and timed out on input 1.0, indicating the infinite loop is not fixed."

def test_regression_script():
    path = "/home/user/regression.sh"
    assert os.path.isfile(path), f"The file {path} should exist."
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"The file {path} should be executable."

    # Run regression.sh
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"{path} did not exit with 0. It exited with {result.returncode}."

def test_fuzz_script():
    path = "/home/user/fuzz.sh"
    assert os.path.isfile(path), f"The file {path} should exist."
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"The file {path} should be executable."

    # Run fuzz.sh
    try:
        result = subprocess.run([path], capture_output=True, text=True, timeout=60)
        assert result.returncode == 0, f"{path} did not exit with 0. It exited with {result.returncode}."
    except subprocess.TimeoutExpired:
        assert False, f"{path} timed out. It should complete all 50 runs successfully."