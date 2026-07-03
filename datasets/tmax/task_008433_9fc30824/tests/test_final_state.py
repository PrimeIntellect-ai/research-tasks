# test_final_state.py

import os
import stat
import subprocess

def test_stealth_auth_c_exists():
    c_path = '/home/user/stealth_auth.c'
    assert os.path.isfile(c_path), f"The source file {c_path} does not exist."

def test_stealth_auth_executable_exists():
    exe_path = '/home/user/stealth_auth'
    assert os.path.isfile(exe_path), f"The executable {exe_path} does not exist."
    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"The file {exe_path} is not executable."

def test_stealth_auth_execution():
    exe_path = '/home/user/stealth_auth'
    log_path = '/home/user/auth_result.log'

    # Ensure log doesn't exist from a previous run or remove it
    if os.path.exists(log_path):
        os.remove(log_path)

    # The hex string for "sysadmin_secret_991" XORed with 0x7F
    hex_input = "0c060c1e1b121611200c1a1c0d1a0b2046464e\n"

    try:
        process = subprocess.run(
            [exe_path],
            input=hex_input,
            text=True,
            capture_output=True,
            timeout=5
        )
    except Exception as e:
        assert False, f"Failed to execute {exe_path}: {e}"

    assert os.path.isfile(log_path), f"The log file {log_path} was not created after running the executable."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "ACCESS_GRANTED", f"Expected 'ACCESS_GRANTED' in {log_path}, but got '{content}'."