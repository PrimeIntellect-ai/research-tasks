# test_final_state.py
import os

def test_analyze_chain_script_exists_and_executable():
    script_path = "/home/user/analyze_chain.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_auth_db_chain_log_exists():
    log_path = "/home/user/auth_db_chain.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist. Did you run the script for auth_db?"
    assert os.path.isfile(log_path), f"Path {log_path} is not a file."

def test_auth_db_chain_log_content():
    log_path = "/home/user/auth_db_chain.log"
    if not os.path.exists(log_path):
        return  # Handled by previous test

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Target DB: auth_db",
        "Base Backup: b4",
        "Chain: b4 -> b5 -> b6 -> b7 -> b8",
        "Total Size: 2784"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == 4, f"Expected 4 lines in {log_path}, found {len(actual_lines)}."

    for i, expected in enumerate(expected_lines):
        assert actual_lines[i] == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual_lines[i]}'"