# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE = "/home/user/math-ci"

def test_success_log_exists_and_correct():
    success_log_path = os.path.join(WORKSPACE, "success.log")
    assert os.path.isfile(success_log_path), f"Expected file {success_log_path} does not exist."
    with open(success_log_path, "r") as f:
        content = f.read().strip()
    assert content == "CI_PIPELINE_FIXED", f"Expected success.log to contain exactly 'CI_PIPELINE_FIXED', but got '{content}'."

def test_libmathvm_so_exists():
    so_path = os.path.join(WORKSPACE, "libmathvm.so")
    assert os.path.isfile(so_path), f"Shared library {so_path} was not built."

def test_vm_c_bug_fixed():
    vm_c_path = os.path.join(WORKSPACE, "vm.c")
    assert os.path.isfile(vm_c_path), f"File {vm_c_path} is missing."
    with open(vm_c_path, "r") as f:
        content = f.read()
    # The original bug was `stack[sp++] = a - b;` where `a` was the top of the stack and `b` was the element below it.
    # The fix should result in `b - a` being pushed to the stack.
    assert "a - b" not in content.replace(" ", ""), "The logic bug in vm.c (subtracting in the wrong order) does not appear to be fixed."
    assert "b-a" in content.replace(" ", "") or "-a" in content.replace(" ", ""), "The subtraction logic in vm.c does not appear to reflect the correct order (b - a)."

def test_go_test_passes():
    env = os.environ.copy()
    # Set LD_LIBRARY_PATH so the go test can find libmathvm.so
    current_ld = env.get("LD_LIBRARY_PATH", "")
    env["LD_LIBRARY_PATH"] = f"{WORKSPACE}:{current_ld}" if current_ld else WORKSPACE

    try:
        result = subprocess.run(
            ["go", "test", "-v"],
            cwd=WORKSPACE,
            env=env,
            capture_output=True,
            text=True,
            timeout=30
        )
    except FileNotFoundError:
        pytest.fail("The 'go' command was not found.")
    except subprocess.TimeoutExpired:
        pytest.fail("The 'go test' command timed out.")

    assert result.returncode == 0, f"'go test' failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"