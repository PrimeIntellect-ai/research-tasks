# test_final_state.py

import os
import subprocess

def test_vm_cpp_exists():
    assert os.path.isfile("/home/user/vm.cpp"), "/home/user/vm.cpp is missing."

def test_vm_executable_exists():
    assert os.path.isfile("/home/user/vm"), "/home/user/vm is missing."
    assert os.access("/home/user/vm", os.X_OK), "/home/user/vm is not executable."

def test_test_success_asm():
    path = "/home/user/test_success.asm"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) <= 10, f"{path} contains more than 10 instructions."

def test_test_limit_asm():
    path = "/home/user/test_limit.asm"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    assert len(lines) == 12, f"{path} does not contain exactly 12 instructions."

def test_run_ci_sh():
    path = "/home/user/run_ci.sh"
    assert os.path.isfile(path), f"{path} is missing."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_ci_summary_txt():
    path = "/home/user/ci_summary.txt"
    assert os.path.isfile(path), f"{path} is missing."
    with open(path, "r") as f:
        content = f.read()

    assert "SUCCESS_TEST_OUTPUT: 15" in content, "SUCCESS_TEST_OUTPUT: 15 not found in ci_summary.txt"
    assert "LIMIT_TEST_EXIT_CODE: 42" in content, "LIMIT_TEST_EXIT_CODE: 42 not found in ci_summary.txt"

def test_vm_behavior_limit():
    # Run the VM against test_limit.asm directly to ensure it actually enforces the limit
    result = subprocess.run(
        ["/home/user/vm", "/home/user/test_limit.asm"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 42, f"VM did not exit with code 42 on limit test. Exit code was {result.returncode}"
    assert "QUOTA_EXCEEDED" in result.stderr, "VM did not print QUOTA_EXCEEDED to stderr."

def test_vm_behavior_success():
    # Run the VM against test_success.asm
    result = subprocess.run(
        ["/home/user/vm", "/home/user/test_success.asm"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"VM did not exit with code 0 on success test. Exit code was {result.returncode}"
    assert result.stdout.strip() == "15", f"VM did not output 15 on success test. Output was {result.stdout.strip()}"