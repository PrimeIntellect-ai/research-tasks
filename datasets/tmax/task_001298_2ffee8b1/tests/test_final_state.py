# test_final_state.py

import os
import subprocess
import pytest

def test_e2e_script_exists_and_executable():
    script_path = "/home/user/e2e.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_e2e_script_execution_and_output():
    script_path = "/home/user/e2e.sh"
    output_log = "/home/user/output.log"

    # Remove output.log if it exists to ensure a fresh run
    if os.path.exists(output_log):
        os.remove(output_log)

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True, cwd="/home/user")

    assert result.returncode == 0, f"e2e.sh exited with non-zero status code: {result.returncode}\nStderr: {result.stderr}"

    assert os.path.isfile(output_log), f"output.log was not created at {output_log}"

    with open(output_log, 'r') as f:
        content = f.read()

    expected_artifacts = ["Processed: core", "Processed: utils", "Processed: app"]
    for artifact in expected_artifacts:
        assert artifact in content, f"Expected '{artifact}' in output.log, but it was not found. Content:\n{content}"