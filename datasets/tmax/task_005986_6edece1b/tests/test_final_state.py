# test_final_state.py
import os
import ast
import hashlib

def test_exploit_script_exists_and_valid():
    """Check if the exploit script exists and contains valid Python code."""
    exploit_path = '/home/user/exploit.py'
    assert os.path.isfile(exploit_path), f"{exploit_path} does not exist."

    with open(exploit_path, 'r') as f:
        code = f.read()

    try:
        ast.parse(code)
    except SyntaxError as e:
        assert False, f"{exploit_path} contains invalid Python code: {e}"

def test_flag_file_correct():
    """Check if the flag file contains the exact expected flag."""
    flag_path = '/home/user/flag.txt'
    assert os.path.isfile(flag_path), f"{flag_path} does not exist."

    with open(flag_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{pwn3d_th3_c0py_p4st3_s3rv1c3}"
    assert content == expected_flag, f"Flag file does not contain the correct flag. Found: {content}"

def test_flag_hash_file_correct():
    """Check if the flag hash file contains the correct SHA-256 digest."""
    hash_path = '/home/user/flag_hash.txt'
    assert os.path.isfile(hash_path), f"{hash_path} does not exist."

    with open(hash_path, 'r') as f:
        content = f.read().strip()

    expected_flag = b"FLAG{pwn3d_th3_c0py_p4st3_s3rv1c3}"
    expected_hash = hashlib.sha256(expected_flag).hexdigest()

    assert content == expected_hash, f"Flag hash file does not contain the correct SHA-256 hash. Found: {content}"