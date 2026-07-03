# test_final_state.py

import os
import json

def test_generate_audit_script_exists_and_executable():
    script_path = "/home/user/generate_audit.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_audit_report_json_content():
    report_path = "/home/user/audit_report.json"
    assert os.path.isfile(report_path), f"The audit report {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    assert report_data.get("jwt_bypass_successful") is True, "The 'jwt_bypass_successful' field is missing or not True."
    assert report_data.get("admin_secret") == "FLAG{jwt_bypass_successful_9921}", "The 'admin_secret' field does not match the expected secret data."
    assert report_data.get("sqli_response_code") == 500, "The 'sqli_response_code' field does not match the expected HTTP status code (500)."

    expected_xss_body = "<html><body>Results for <script>alert('audit')</script></body></html>"
    assert report_data.get("xss_response_body") == expected_xss_body, "The 'xss_response_body' field does not match the expected raw response body."