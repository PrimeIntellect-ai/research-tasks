# test_final_state.py

import os
import json

def test_report_json_exists_and_correct():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), "report.json does not exist. The script might not have run successfully."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "report.json does not contain valid JSON."

    assert data.get("status") == "success", f"Expected status 'success', got '{data.get('status')}'."
    assert data.get("secret") == "DIAG-SEC-77bbx9", f"Incorrect secret recovered. Got '{data.get('secret')}'."

    port = data.get("port")
    assert port == 8088 or port == "8088", f"Incorrect port extracted from pcap. Got '{port}'."

def test_combined_log_contains_all_entries():
    combined_log_path = "/home/user/diag-tool/combined.log"
    assert os.path.exists(combined_log_path), "combined.log was not generated. The script might have failed."

    with open(combined_log_path, "r") as f:
        content = f.read()

    assert "ERROR 55: Critical failure in processing" in content, (
        "The combined.log does not contain the error message from 'error log 1.txt'. "
        "The bash script loop was likely not fixed correctly to handle spaces in filenames."
    )
    assert "System initialized" in content, "The combined.log does not contain the entry from 'system log.txt'."
    assert "Normal log entry" in content, "The combined.log does not contain the entry from 'app_log.txt'."

def test_env_file_updated():
    env_path = "/home/user/diag-tool/.env"
    assert os.path.exists(env_path), ".env file is missing."

    with open(env_path, "r") as f:
        content = f.read()

    assert "SECRET=DIAG-SEC-77bbx9" in content, "The .env file does not contain the correct recovered SECRET."
    assert "PORT=8088" in content, "The .env file does not contain the correct extracted PORT."