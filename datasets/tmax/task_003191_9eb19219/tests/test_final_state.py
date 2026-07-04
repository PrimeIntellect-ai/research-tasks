# test_final_state.py

import os

def test_violation_path_output():
    output_path = "/home/user/violation_path.txt"
    assert os.path.exists(output_path), f"Missing output file: {output_path}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_path = "U73,R10,R12,R14,R16,RES-999"
    assert content == expected_path, f"Incorrect violation path in {output_path}. Expected '{expected_path}', got '{content}'"

def test_audit_rs_exists():
    source_path = "/home/user/audit.rs"
    assert os.path.exists(source_path), f"Missing Rust source file: {source_path}"