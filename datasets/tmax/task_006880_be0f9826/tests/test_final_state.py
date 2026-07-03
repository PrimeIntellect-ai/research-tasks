# test_final_state.py
import os
import subprocess
import pytest

def test_audit_plugin_script_exists_and_executable():
    script_path = "/home/user/audit_plugin.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_execution_and_outputs():
    script_path = "/home/user/audit_plugin.sh"

    # Execute the script as the user to ensure it performs the required actions
    result = subprocess.run(["sudo", "-u", "user", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}\nstdout: {result.stdout}"

    # 1. Verify Makefile was fixed
    makefile_path = "/home/user/src/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} does not exist."
    with open(makefile_path, "r") as f:
        makefile_content = f.read()
    assert "\t" in makefile_content, "Makefile does not use tabs for the build recipe."
    assert "-shared" in makefile_content, "Makefile is missing the -shared flag."

    # 2. Verify auth_plugin.so was built
    so_path = "/home/user/src/auth_plugin.so"
    assert os.path.isfile(so_path), f"Shared object {so_path} was not built."

    # 3. Verify assembly analysis (syscall count)
    count_path = "/home/user/syscall_count.txt"
    assert os.path.isfile(count_path), f"{count_path} does not exist."
    with open(count_path, "r") as f:
        count = f.read().strip()
    assert count == "1", f"Expected syscall count to be '1', but got '{count}'."

    # 4 & 5. Verify runner.c, executable, and execution.log
    runner_c_path = "/home/user/runner.c"
    runner_path = "/home/user/runner"
    assert os.path.isfile(runner_c_path), f"Runner source {runner_c_path} does not exist."
    assert os.path.isfile(runner_path), f"Runner executable {runner_path} does not exist."

    log_path = "/home/user/execution.log"
    assert os.path.isfile(log_path), f"Execution log {log_path} does not exist."
    with open(log_path, "r") as f:
        log_content = f.read().strip()

    # The validate function returns 42
    assert log_content == "42", f"Expected execution output to be '42', but got '{log_content}'."