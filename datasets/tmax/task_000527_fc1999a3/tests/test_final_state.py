# test_final_state.py

import os

def test_audit_result_exists_and_correct():
    file_path = "/home/user/audit_result.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you run your script and save the output?"

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_flag = "FLAG{devsecops_jwt_audited_8912}"
    assert content == expected_flag, f"The content of {file_path} is incorrect. Expected '{expected_flag}', got '{content}'."