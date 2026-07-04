# test_final_state.py
import os
import re

def test_recovered_log_file():
    log_path = "/home/user/recovered_app.log"
    assert os.path.exists(log_path), f"Recovered log file {log_path} is missing."

    with open(log_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 1000, f"Recovered log file should have exactly 1000 lines, but has {len(lines)}."

    # Check line 734 (index 733)
    expected_critical = "[ERROR] CRITICAL_FAILURE_DB_CONNECTION_DROPPED"
    assert expected_critical in lines[733], "Line 734 does not contain the expected critical failure message."

    # Check line 1 (index 0)
    expected_info = "[INFO] Processed request 1 successfully."
    assert expected_info in lines[0], "Line 1 does not contain the expected info message."

def test_env_file_fixed():
    env_path = "/home/user/.env"
    assert os.path.exists(env_path), f"Environment file {env_path} is missing."

    with open(env_path, "r") as f:
        content = f.read()

    # Extract MAX_RETRIES value
    match = re.search(r'export MAX_RETRIES=["\']?(.*?)["\']?(?:\n|$)', content)
    assert match is not None, "MAX_RETRIES variable is missing from .env"

    val = match.group(1)
    try:
        int_val = int(val)
    except ValueError:
        assert False, f"MAX_RETRIES value '{val}' is not a valid integer. The misconfiguration was not fixed."

def test_report_generated():
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} is missing. Did you run the script?"

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "INFO_COUNT=999\nCRITICAL_COUNT=1\nSUCCESS"
    assert content == expected_content, f"Report file contents are incorrect. Expected:\n{expected_content}\nGot:\n{content}"