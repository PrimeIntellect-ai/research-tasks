# test_final_state.py

import os
import time
import json
import subprocess

def test_audit_summary_exists_and_valid():
    output_file = "/home/user/audit_summary.json"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. Did you run the script and save the output?"

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {output_file} is not valid JSON."

def test_run_audit_speed():
    script_file = "/home/user/run_audit.py"
    assert os.path.isfile(script_file), f"Script file {script_file} does not exist."

    start = time.time()
    result = subprocess.run(["python", script_file], capture_output=True, text=True)
    elapsed = time.time() - start

    assert result.returncode == 0, f"Script failed to run. Return code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert elapsed < 2.0, f"Speedup not achieved. Took {elapsed:.2f} seconds, expected < 2.0s. The query optimization is not sufficient or the index was not used."