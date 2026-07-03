# test_final_state.py

import os
import json
import pytest

def test_scan_report_exists():
    report_path = '/home/user/scan_report.json'
    assert os.path.isfile(report_path), f"Scan report not found at {report_path}. Ensure your C++ program generates this file."

def test_scan_report_score():
    report_path = '/home/user/scan_report.json'
    assert os.path.isfile(report_path), f"Scan report not found at {report_path}."

    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse {report_path} as JSON: {e}")

    expected_token = "s3cr3t_p4ss"
    expected_flag = "FLAG{vulpix_scan_99}"

    score = 0.0
    actual_token = data.get("token")
    actual_flag = data.get("flag")

    if actual_token == expected_token:
        score += 0.5
    if actual_flag == expected_flag:
        score += 0.5

    assert score >= 0.95, (
        f"Detection score is {score}, which is below the threshold of 0.95. "
        f"Extracted token: '{actual_token}', Extracted flag: '{actual_flag}'."
    )

def test_nginx_config_updated():
    nginx_conf_path = '/app/nginx/nginx.conf'
    assert os.path.isfile(nginx_conf_path), f"Nginx config not found at {nginx_conf_path}"

    with open(nginx_conf_path, 'r') as f:
        content = f.read()

    assert "5000" in content, (
        "Nginx configuration does not appear to be updated to proxy requests to the Flask API on port 5000."
    )