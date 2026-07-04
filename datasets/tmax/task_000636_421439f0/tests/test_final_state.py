# test_final_state.py
import os
import stat
import pytest

def test_vnc_endpoints_log():
    log_path = "/home/user/logs/vnc_endpoints.log"
    assert os.path.isfile(log_path), f"Error: {log_path} does not exist."

    with open(log_path, "r") as f:
        actual_content = f.read().strip()

    expected_content = (
        "VM_ID: 101 | VNC: 192.168.1.50:5901\n"
        "VM_ID: 102 | VNC: 10.0.0.5:5902\n"
        "VM_ID: 104 | VNC: 127.0.0.1:5900"
    )

    assert actual_content == expected_content, (
        f"Output mismatch in {log_path}.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )

def test_hook_permissions():
    hook_path = "/home/user/git_server/migration.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Error: Hook file {hook_path} does not exist."

    st = os.stat(hook_path)
    perms = stat.S_IMODE(st.st_mode)

    assert perms == 0o700, f"Error: Hook permissions are {oct(perms)}, expected 0o700."

def test_compiled_binary_exists_and_executable():
    binary_path = "/home/user/build_env/vnc_parser"
    assert os.path.isfile(binary_path), f"Error: Compiled binary {binary_path} not found."

    assert os.access(binary_path, os.X_OK), f"Error: Compiled binary {binary_path} is not executable."