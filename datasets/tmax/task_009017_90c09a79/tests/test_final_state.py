# test_final_state.py
import os
import importlib.util

def test_flag_file_exists_and_correct():
    flag_path = '/home/user/flag.txt'
    assert os.path.exists(flag_path), f"File {flag_path} does not exist. Did you save the output?"

    with open(flag_path, 'r') as f:
        content = f.read().strip()

    expected_flag = "FLAG{num3r1c4l_4n4lys1s_ftw}"
    assert expected_flag in content, f"Contents of {flag_path} are incorrect. Found: {content}"

def test_decrypt_script_fixes():
    script_path = '/home/user/decrypt_payload.py'
    assert os.path.exists(script_path), f"Python script {script_path} does not exist."

    # Dynamically load the student's script to test the functions directly
    spec = importlib.util.spec_from_file_location("decrypt_payload", script_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        assert False, f"Failed to import {script_path} due to syntax or runtime error: {e}"

    # Verify SQL fix
    assert hasattr(module, 'get_latest_salt'), "Function 'get_latest_salt' is missing."
    try:
        salt = module.get_latest_salt(8472)
    except Exception as e:
        assert False, f"Error calling get_latest_salt(8472): {e}"

    assert salt == 1e-08, f"get_latest_salt(8472) returned {salt}, expected 1e-08. The SQL query is likely not fetching the most recently created salt."

    # Verify numerical instability fix
    assert hasattr(module, 'derive_key'), "Function 'derive_key' is missing."
    try:
        key = module.derive_key(1e-08)
    except Exception as e:
        assert False, f"Error calling derive_key(1e-08): {e}"

    assert key != 0, "derive_key(1e-08) returned 0. The numerical instability (catastrophic cancellation) has not been fixed."
    assert key == 500000, f"derive_key(1e-08) returned {key}, expected 500000. The mathematical formula is incorrect."