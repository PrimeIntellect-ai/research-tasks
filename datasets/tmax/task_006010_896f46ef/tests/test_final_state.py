# test_final_state.py

import os
import pytest

def test_forged_jwt_exists_and_correct():
    jwt_path = "/home/user/forged.jwt"
    assert os.path.isfile(jwt_path), f"File {jwt_path} does not exist. Did you save the forged token?"

    with open(jwt_path, "r") as f:
        content = f.read().strip()

    expected_jwt = "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiYWRtaW4iLCJyb2xlIjoic3VwZXJfYWRtaW5pc3RyYXRvcl85OTIifQ."

    assert content == expected_jwt, (
        "The forged JWT in /home/user/forged.jwt is incorrect. "
        "Ensure you used the 'none' algorithm, set user to 'admin', "
        "set the correct hidden role, and properly base64url-encoded the payload without padding."
    )

def test_flag_file_exists_and_correct():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"File {flag_path} does not exist. Did you run auth_checker and save its output?"

    with open(flag_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{alg_none_bypass_success_8812}"

    assert expected_flag in content, (
        f"The flag in {flag_path} is incorrect or missing. "
        "Did you pass the correct forged JWT to the auth_checker binary?"
    )

def test_forge_script_exists():
    script_path = "/home/user/forge.py"
    assert os.path.isfile(script_path), f"Python script {script_path} does not exist. Did you write the script as requested?"