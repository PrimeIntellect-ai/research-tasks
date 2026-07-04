# test_final_state.py
import os

def test_server_db_log_contents():
    log_path = "/home/user/server_db.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. The pipeline may not have run successfully."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "ADD_USER jdoe AS editor",
        "ADD_USER asmith AS viewer",
        "ADD_USER tjones AS admin"
    ]

    assert lines == expected_lines, f"Contents of {log_path} do not match expected output. Got: {lines}"

def test_required_files_exist():
    required_files = [
        "/home/user/parser.cpp",
        "/home/user/run_pipeline.sh",
        "/home/user/interact.exp"
    ]

    for file_path in required_files:
        assert os.path.exists(file_path), f"Required file {file_path} is missing."