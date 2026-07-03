# test_final_state.py
import os
import subprocess

def test_executable_exists():
    exe_path = "/home/user/metrics_tool/metrics_tool"
    assert os.path.isfile(exe_path), f"{exe_path} executable not found. Did make run successfully?"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_test_results_log():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} not found. Did you run the test script and redirect its output?"
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "ALL_TESTS_PASS", f"Expected 'ALL_TESTS_PASS' in {log_path}, got '{content}'"

def test_metrics_tool_output():
    tool_path = "/home/user/metrics_tool/metrics_tool"
    input_data = "1,10.0\n1,20.0\n1,30.0\n2,40.0\n"
    expected_output = "1,10.00\n1,15.00\n1,RATE_LIMIT_EXCEEDED\n2,23.33\n"

    process = subprocess.Popen(
        [tool_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate(input=input_data)

    assert process.returncode == 0, f"metrics_tool exited with non-zero status: {process.returncode}. Stderr: {stderr}"
    assert stdout == expected_output, f"metrics_tool output mismatch.\nExpected:\n{expected_output}\nGot:\n{stdout}"