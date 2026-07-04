# test_final_state.py
import os
import json

def test_forensics_report_exists_and_valid():
    report_path = "/home/user/forensics_report.json"
    assert os.path.isfile(report_path), f"The report file {report_path} was not created."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    assert "c2_ip" in data, "Missing 'c2_ip' in report."
    assert data["c2_ip"] == "192.168.100.55", f"Incorrect c2_ip. Expected '192.168.100.55', got '{data['c2_ip']}'."

    assert "c2_port" in data, "Missing 'c2_port' in report."
    assert int(data["c2_port"]) == 8443, f"Incorrect c2_port. Expected 8443, got {data['c2_port']}."

    assert "auth_cookie" in data, "Missing 'auth_cookie' in report."
    assert "MaliciousToken-7712" in data["auth_cookie"], f"Incorrect auth_cookie. Expected it to contain 'MaliciousToken-7712', got '{data['auth_cookie']}'."

    assert "custom_header_name" in data, "Missing 'custom_header_name' in report."
    assert data["custom_header_name"] == "X-Data-Exfil", f"Incorrect custom_header_name. Expected 'X-Data-Exfil', got '{data['custom_header_name']}'."

    assert "compromised_file" in data, "Missing 'compromised_file' in report."
    assert "config_C.conf" in data["compromised_file"], f"Incorrect compromised_file. Expected 'config_C.conf', got '{data['compromised_file']}'."

    assert "decoded_payload" in data, "Missing 'decoded_payload' in report."
    assert data["decoded_payload"] == "SecretForensicsData_992", f"Incorrect decoded_payload. Expected 'SecretForensicsData_992', got '{data['decoded_payload']}'."

def test_go_script_exists():
    script_path = "/home/user/forensics.go"
    assert os.path.isfile(script_path), f"The Go script {script_path} was not found."