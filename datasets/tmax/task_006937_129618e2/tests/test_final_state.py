# test_final_state.py

import os
import subprocess

def test_script_exists_and_executable():
    script_path = "/home/user/detect_cycles.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_execution_and_output():
    script_path = "/home/user/detect_cycles.sh"

    # Execute the script to ensure it performs the workflow
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    db_path = "/home/user/graph.db"
    assert os.path.isfile(db_path), f"Database {db_path} was not created by the script."

    out_path = "/home/user/cycle_summary.csv"
    assert os.path.isfile(out_path), f"Output file {out_path} was not created by the script."

    with open(out_path, "r") as f:
        content = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected_content = [
        "name,total_outgoing_cycle_amount",
        "Alice,1200",
        "Bob,700",
        "Charlie,1700",
        "David,1000"
    ]

    assert content == expected_content, f"Output CSV content does not match expected.\nExpected: {expected_content}\nGot: {content}"