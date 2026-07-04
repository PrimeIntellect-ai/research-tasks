# test_final_state.py

import os
import subprocess

def test_verification_log_success():
    log_path = "/home/user/math_port/verification.log"
    assert os.path.isfile(log_path), f"Verification log {log_path} does not exist. Did you run the python script?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "SUCCESS", f"Expected verification log to contain 'SUCCESS', but found: '{content}'"

def test_executable_is_statically_linked():
    exe_path = "/home/user/math_port/det_calc"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did you compile the code?"

    # Use the 'file' command to check if it's statically linked
    result = subprocess.run(["file", exe_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run 'file' command on {exe_path}"

    output = result.stdout.lower()
    assert "statically linked" in output, f"Executable {exe_path} is not statically linked. Output of 'file': {output}"

def test_makefile_exists():
    makefile_path = "/home/user/math_port/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile at {makefile_path} does not exist."