# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_makefile_contains_lm():
    makefile_path = "/home/user/project/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile {makefile_path} does not exist."
    with open(makefile_path, "r") as f:
        content = f.read()
    assert "-lm" in content, f"Makefile does not contain '-lm' for linking the math library."

def test_pipeline_execution_and_outputs():
    # Run the pipeline script
    script_path = "/home/user/pipeline.sh"
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed to execute. stderr: {result.stderr}"

    # Check status.log
    status_log_path = "/home/user/status.log"
    assert os.path.isfile(status_log_path), f"{status_log_path} does not exist."
    with open(status_log_path, "r") as f:
        status = f.read().strip()
    assert status == "PASS", f"Expected 'PASS' in {status_log_path}, but got '{status}'"

    # Check asm_line_count.txt
    asm_count_path = "/home/user/asm_line_count.txt"
    assert os.path.isfile(asm_count_path), f"{asm_count_path} does not exist."
    with open(asm_count_path, "r") as f:
        count_str = f.read().strip()

    # Extract the first word/number in case it contains filename (e.g., '123 main.s')
    count_val = count_str.split()[0] if count_str else ""
    assert count_val.isdigit(), f"{asm_count_path} does not contain a valid integer. Found: '{count_str}'"

    # Check final_output.txt matches expected.txt
    final_output_path = "/home/user/final_output.txt"
    expected_path = "/home/user/project/expected.txt"
    assert os.path.isfile(final_output_path), f"{final_output_path} does not exist."
    assert os.path.isfile(expected_path), f"{expected_path} does not exist."

    with open(final_output_path, "r") as f:
        final_content = f.read().strip()
    with open(expected_path, "r") as f:
        expected_content = f.read().strip()

    assert final_content == expected_content, "final_output.txt does not match expected.txt"