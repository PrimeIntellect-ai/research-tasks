# test_final_state.py

import os
import subprocess
import pytest

def test_exploit_gen_c_exists():
    """Verify that the student wrote the exploit generator source code."""
    file_path = "/home/user/exploit_gen.c"
    assert os.path.exists(file_path), f"Required file is missing: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"

def test_malicious_session_exists():
    """Verify that the malicious session file was generated."""
    file_path = "/home/user/malicious_session.txt"
    assert os.path.exists(file_path), f"Required file is missing: {file_path}"
    assert os.path.isfile(file_path), f"Path exists but is not a file: {file_path}"

def test_exploit_success():
    """
    Verify that the exploit works by compiling the router, running it with
    the generated session file, and checking the output.
    """
    router_c = "/home/user/router.c"
    router_bin = "/home/user/router"
    session_file = "/home/user/malicious_session.txt"
    hacked_file = "/home/user/hacked.txt"

    assert os.path.exists(router_c), f"Router source code missing: {router_c}"
    assert os.path.exists(session_file), f"Session file missing: {session_file}"

    # Clean up any existing hacked.txt to ensure we are testing the current run
    if os.path.exists(hacked_file):
        os.remove(hacked_file)

    # Compile the router
    compile_cmd = ["gcc", "-o", router_bin, router_c]
    compile_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_proc.returncode == 0, f"Failed to compile {router_c}:\n{compile_proc.stderr}"

    # Run the router with the malicious session file
    run_cmd = [router_bin, session_file]
    run_proc = subprocess.run(run_cmd, cwd="/home/user", capture_output=True, text=True)

    # The router might return non-zero if the shell command fails after our injected command,
    # but the primary check is whether hacked.txt was created properly.

    assert os.path.exists(hacked_file), "The exploit failed: /home/user/hacked.txt was not created."

    with open(hacked_file, "r") as f:
        content = f.read().strip()

    assert content == "PWNED", f"The exploit failed: /home/user/hacked.txt contains '{content}' instead of 'PWNED'."