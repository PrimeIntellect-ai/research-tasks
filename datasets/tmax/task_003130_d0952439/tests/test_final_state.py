# test_final_state.py

import os
import subprocess
import pytest

def test_eval_graph_compiled_and_executable():
    """Verify that eval_graph has been compiled and is executable."""
    exe_path = "/home/user/qa_env/eval_graph"
    assert os.path.isfile(exe_path), f"File {exe_path} does not exist. Did you compile the C program?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_eval_graph_correct_precedence():
    """Verify that eval_graph correctly evaluates math expressions with proper precedence."""
    exe_path = "/home/user/qa_env/eval_graph"
    assert os.path.isfile(exe_path), f"File {exe_path} does not exist."

    # Test case: 2+3*4 should be 14, not 20
    input_data = "START END 2+3*4\n"
    process = subprocess.run([exe_path], input=input_data, text=True, capture_output=True)
    assert process.returncode == 0, "eval_graph crashed or returned non-zero exit code."

    output = process.stdout.strip()
    assert output == "14", f"Expected eval_graph to output 14 for 2+3*4, but got {output}. Precedence bug might not be fixed."

def test_prop_test_sh_exists_and_passes():
    """Verify that prop_test.sh exists, is executable, and passes."""
    script_path = "/home/user/qa_env/prop_test.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

    process = subprocess.run([script_path], capture_output=True, text=True)
    assert process.returncode == 0, f"prop_test.sh failed or returned non-zero exit code.\nStdout: {process.stdout}\nStderr: {process.stderr}"

def test_qa_report_content():
    """Verify that qa_report.txt contains the correct shortest path."""
    report_path = "/home/user/qa_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    with open(report_path, 'r') as f:
        content = f.read().strip()

    assert content == "22", f"Expected qa_report.txt to contain '22', but got '{content}'."