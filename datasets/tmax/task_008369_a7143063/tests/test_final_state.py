# test_final_state.py

import os
import subprocess

def test_total_errors_count():
    filepath = "/home/user/total_errors.txt"
    assert os.path.isfile(filepath), f"{filepath} does not exist. Did you run the script?"

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content == "3", f"Expected total errors to be 3, but got {content}. Check if process_logs.sh processes all files and process.py handles corrupted files correctly."

def test_mre_script_exists():
    filepath = "/home/user/mre.py"
    assert os.path.isfile(filepath), f"MRE script {filepath} does not exist."

def test_mre_script_execution():
    filepath = "/home/user/mre.py"
    assert os.path.isfile(filepath), f"MRE script {filepath} does not exist."

    result = subprocess.run(["python3", filepath], capture_output=True, text=True)

    assert result.returncode == 0, f"MRE script exited with non-zero code {result.returncode}.\nStderr: {result.stderr}"
    assert "Traceback interpreted correctly" in result.stdout, "MRE script did not output 'Traceback interpreted correctly' as expected."