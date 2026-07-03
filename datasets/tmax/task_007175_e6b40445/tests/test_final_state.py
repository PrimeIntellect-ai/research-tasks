# test_final_state.py

import os
import stat
import pytest

def test_ssh_keys_permissions():
    keys_dir = "/home/user/ssh_keys"
    assert os.path.isdir(keys_dir), f"Directory {keys_dir} does not exist."

    files = os.listdir(keys_dir)
    assert len(files) > 0, f"No files found in {keys_dir}."

    for filename in files:
        filepath = os.path.join(keys_dir, filename)
        if os.path.isfile(filepath):
            st = os.stat(filepath)
            perms = oct(st.st_mode)[-3:]
            assert perms == "600", f"File {filepath} has incorrect permissions: {perms} (expected 600)."

def test_pwned_file_exists_and_content():
    pwned_file = "/home/user/pwned.txt"
    assert os.path.isfile(pwned_file), f"File {pwned_file} does not exist."

    with open(pwned_file, "r") as f:
        content = f.read().strip()

    assert content == "SERVICE_COMPROMISED", f"File {pwned_file} contains '{content}', expected 'SERVICE_COMPROMISED'."

def test_exploit_script_exists_and_valid():
    exploit_file = "/home/user/exploit.py"
    assert os.path.isfile(exploit_file), f"File {exploit_file} does not exist."

    with open(exploit_file, "r") as f:
        source = f.read()

    try:
        compile(source, exploit_file, 'exec')
    except SyntaxError as e:
        pytest.fail(f"File {exploit_file} is not a valid Python script. SyntaxError: {e}")