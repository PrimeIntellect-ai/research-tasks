# test_final_state.py
import os

def test_validation_log_success():
    log_path = "/home/user/telemetry_broker/validation.log"
    assert os.path.isfile(log_path), f"The validation log file {log_path} is missing. Did you run the test_runner.py script?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_string = "SUCCESS: All tests passed."
    assert expected_string in content, f"The validation log does not contain the expected success message. Found: {content}"

def test_executable_exists():
    executable_path = "/home/user/telemetry_broker/telemetry_broker"
    assert os.path.isfile(executable_path), f"The compiled executable {executable_path} is missing. Did you run make?"
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."