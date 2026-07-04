# test_final_state.py

import os
import subprocess
import pytest

def test_corrupted_payload_extracted():
    payload_file = "/home/user/corrupted_payload.json"
    assert os.path.exists(payload_file), f"File {payload_file} does not exist."

    with open(payload_file, "r") as f:
        content = f.read()

    # The corrupted payload is exactly '{"amount": 15,'
    assert content == '{"amount": 15,', f"Expected corrupted payload to be exactly '{{\"amount\": 15,', but got {repr(content)}"

def test_summary_result():
    result_file = "/home/user/summary_result.txt"
    assert os.path.exists(result_file), f"File {result_file} does not exist."

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert content == "16777219.00", f"Expected summary result to be '16777219.00', but got '{content}'"

def test_process_tx_fixed():
    script_path = "/home/user/process_tx.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."

    input_data = '{"amount": 1}\n{"bad": \n{"amount": 2}\n'

    result = subprocess.run(
        ["python3", script_path],
        input=input_data,
        text=True,
        capture_output=True
    )

    assert result.returncode == 0, f"process_tx.py exited with error code {result.returncode}. stderr: {result.stderr}"

    stdout_lines = [line.strip() for line in result.stdout.strip().split("\n")]

    assert "Processed: 1" in stdout_lines, "Expected 'Processed: 1' in output."
    assert "Error: Corrupted input" in stdout_lines, "Expected 'Error: Corrupted input' in output."
    assert "Processed: 2" in stdout_lines, "Expected 'Processed: 2' in output."