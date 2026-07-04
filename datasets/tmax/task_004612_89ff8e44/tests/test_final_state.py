# test_final_state.py

import os
import stat
import re
import pytest

def test_success_txt():
    success_file = "/home/user/success.txt"
    assert os.path.isfile(success_file), f"File {success_file} does not exist. Did you run the curl command?"

    with open(success_file, "r") as f:
        content = f.read().strip()

    assert content == "Backend operational.", f"Expected 'Backend operational.' in {success_file}, but got '{content}'"

def test_sockets_directory():
    sockets_dir = "/home/user/app/sockets"
    assert os.path.exists(sockets_dir), f"Path {sockets_dir} does not exist."
    assert os.path.isdir(sockets_dir), f"Path {sockets_dir} is not a directory."
    assert not os.path.islink(sockets_dir), f"Path {sockets_dir} is still a symlink."

def test_sockets_permissions():
    sockets_dir = "/home/user/app/sockets"
    assert os.path.exists(sockets_dir), f"Path {sockets_dir} does not exist."

    st = os.stat(sockets_dir)
    perms = oct(st.st_mode)[-3:]
    assert perms == "755", f"Expected permissions 755 for {sockets_dir}, but got {perms}"

def test_bashrc_env():
    bashrc_file = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_file), f"File {bashrc_file} does not exist."

    with open(bashrc_file, "r") as f:
        content = f.read()

    # Check if BACKEND_SOCKET is set to the correct path
    pattern = r"BACKEND_SOCKET\s*=\s*[\"']?/home/user/app/sockets/backend\.sock[\"']?"
    assert re.search(pattern, content), f"BACKEND_SOCKET is not correctly set in {bashrc_file}"

def test_rotate_logs_script():
    script_file = "/home/user/scripts/rotate_logs.sh"
    assert os.path.isfile(script_file), f"File {script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"File {script_file} is not executable."

    with open(script_file, "r") as f:
        content = f.read()

    # Check for mv command
    assert "mv " in content and "error.log" in content and "error.log.1" in content, \
        f"{script_file} does not seem to move error.log to error.log.1"

    # Check for signaling nginx (USR1)
    assert "USR1" in content and ("kill" in content or "nginx -s" in content), \
        f"{script_file} does not seem to send USR1 signal to nginx."