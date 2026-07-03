# test_final_state.py
import os

def test_audit_result_correct():
    path = "/home/user/audit_result.txt"
    assert os.path.isfile(path), f"Missing output file: {path}"

    with open(path, "r") as f:
        content = f.read()

    cleaned_content = content.replace('\n', '').replace('\r', '')
    assert cleaned_content == "Database,4", f"Expected 'Database,4' in {path}, but got '{cleaned_content}'"