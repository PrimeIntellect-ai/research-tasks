# test_final_state.py

import os
import stat
import subprocess

WORKSPACE_DIR = "/home/user/workspace"

def test_mathops_c_patched():
    mathops_path = os.path.join(WORKSPACE_DIR, "mathops.c")
    assert os.path.isfile(mathops_path), f"mathops.c missing at {mathops_path}"
    with open(mathops_path, "r") as f:
        content = f.read()
    assert "return a + b;" in content, "mathops.c was not patched correctly (missing 'return a + b;')"
    assert "return a - b; // BUG!" not in content, "mathops.c still contains the bug"

def test_setup_py_fixed():
    setup_path = os.path.join(WORKSPACE_DIR, "setup.py")
    assert os.path.isfile(setup_path), f"setup.py missing at {setup_path}"
    with open(setup_path, "r") as f:
        content = f.read()
    assert "mathops.c" in content, "setup.py was not fixed to use 'mathops.c'"
    assert "wrong_name.c" not in content, "setup.py still contains 'wrong_name.c'"

def test_test_mathops_py_contents():
    test_path = os.path.join(WORKSPACE_DIR, "test_mathops.py")
    assert os.path.isfile(test_path), f"test_mathops.py missing at {test_path}"
    with open(test_path, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "test_mathops.py does not import hypothesis"
    assert "st.integers()" in content, "test_mathops.py does not use st.integers()"
    assert "mathops" in content, "test_mathops.py does not import mathops"
    assert "test_add" in content, "test_mathops.py does not contain test_add function"

def test_ci_run_sh_executable_and_successful():
    ci_script_path = os.path.join(WORKSPACE_DIR, "ci_run.sh")
    assert os.path.isfile(ci_script_path), f"ci_run.sh missing at {ci_script_path}"

    # Check if executable
    st = os.stat(ci_script_path)
    assert bool(st.st_mode & stat.S_IXUSR), "ci_run.sh is not executable"

    # Run the script
    result = subprocess.run(
        ["./ci_run.sh"],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"ci_run.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"