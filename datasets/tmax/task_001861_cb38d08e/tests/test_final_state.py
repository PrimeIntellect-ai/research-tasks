# test_final_state.py
import os
import json
import hashlib
import base64

def test_security_report_exists_and_valid():
    report_path = '/home/user/security_report.json'
    assert os.path.isfile(report_path), f"{report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{report_path} does not contain valid JSON."

    expected_secret = "S3cr3t_P0licy_K3y_2024!"
    assert report.get("recovered_secret") == expected_secret, "recovered_secret is incorrect."

    assert report.get("sample_token_valid") is True, "sample_token_valid should be true."
    assert report.get("sample_token_policy_failed") is True, "sample_token_policy_failed should be true."

    user = "admin-pipeline"
    csp = "default-src 'self'; script-src 'self';"
    data = expected_secret + user + csp
    sig = hashlib.sha256(data.encode('utf-8')).hexdigest()
    u_b64 = base64.b64encode(user.encode('utf-8')).decode('utf-8')
    c_b64 = base64.b64encode(csp.encode('utf-8')).decode('utf-8')
    expected_token = f"{u_b64}.{c_b64}.{sig}"

    assert report.get("forged_admin_token") == expected_token, "forged_admin_token is incorrect."