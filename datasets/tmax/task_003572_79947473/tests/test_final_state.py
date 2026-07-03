# test_final_state.py

import os
import subprocess
import pytest

def test_problem_file_contents():
    problem_file = "/home/user/problem_file.txt"
    assert os.path.exists(problem_file), f"File {problem_file} does not exist."
    with open(problem_file, "r") as f:
        content = f.read().strip()
    assert content == "/home/user/logs/system_metrics.log", f"Incorrect content in {problem_file}: {content}"

def test_repro_go_behavior():
    repro_script = "/home/user/repro.go"
    assert os.path.exists(repro_script), f"File {repro_script} does not exist."

    # Compile the repro script
    compile_cmd = ["go", "build", "-o", "/tmp/repro", repro_script]
    compile_result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert compile_result.returncode == 0, f"Failed to compile {repro_script}:\n{compile_result.stderr}"

    # Run the compiled binary against the problematic file, it should hang (timeout)
    run_cmd = ["/tmp/repro", "/home/user/logs/system_metrics.log"]
    try:
        subprocess.run(run_cmd, timeout=2, capture_output=True)
        pytest.fail(f"The script {repro_script} did not hang when run against the problematic file. It should block indefinitely.")
    except subprocess.TimeoutExpired:
        # This is expected
        pass

def test_output_log_contents():
    output_log = "/home/user/output.log"
    assert os.path.exists(output_log), f"File {output_log} does not exist."
    with open(output_log, "r") as f:
        content = f.read()
    assert "All logs processed successfully." in content, f"Expected success message not found in {output_log}."

def test_log_processor_go_behavior():
    script_path = "/home/user/log_processor.go"
    assert os.path.exists(script_path), f"File {script_path} does not exist."

    # Run the patched script, it should finish within a short time
    run_cmd = ["go", "run", script_path]
    try:
        result = subprocess.run(run_cmd, timeout=3, capture_output=True, text=True)
        assert result.returncode == 0, f"Script {script_path} failed with return code {result.returncode}:\n{result.stderr}"
        assert "All logs processed successfully." in result.stdout, "Script did not print the expected success message."
    except subprocess.TimeoutExpired:
        pytest.fail(f"The script {script_path} timed out. It is still hanging on the FIFO.")