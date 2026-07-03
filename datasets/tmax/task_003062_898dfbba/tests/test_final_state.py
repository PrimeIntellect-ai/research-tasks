# test_final_state.py
import os

def test_integration_result_log():
    log_path = "/home/user/integration_result.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did the Ruby script run successfully?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected = "Result: 73, Status: 200"
    assert expected in content, f"Log file {log_path} content does not match expected output. Expected to find '{expected}', but got '{content}'"

def test_app_script_exists():
    app_path = "/home/user/app.py"
    assert os.path.isfile(app_path), f"Python API script {app_path} is missing."

def test_ruby_script_exists():
    ruby_path = "/home/user/test_e2e.rb"
    assert os.path.isfile(ruby_path), f"Ruby end-to-end test script {ruby_path} is missing."