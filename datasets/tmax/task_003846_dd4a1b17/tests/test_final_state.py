# test_final_state.py

import json
import os
import pytest

def test_e2e_results_exist_and_correct():
    filepath = "/home/user/calc-feature/e2e_results.json"
    assert os.path.exists(filepath), f"Expected results file {filepath} does not exist."
    assert os.path.isfile(filepath), f"Expected {filepath} to be a file."

    with open(filepath, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {filepath} does not contain valid JSON.")

    assert "status_response" in data, "Missing 'status_response' key in E2E results."
    status_resp = data["status_response"]
    assert isinstance(status_resp, dict), "'status_response' should be a JSON object."
    assert status_resp.get("status") == "ok", f"Expected status 'ok', got {status_resp.get('status')}."
    assert status_resp.get("service") == "auth", f"Expected service 'auth', got {status_resp.get('service')}."

    assert "calc_response" in data, "Missing 'calc_response' key in E2E results."
    calc_resp = data["calc_response"]
    assert isinstance(calc_resp, dict), "'calc_response' should be a JSON object."

    # 10 + 2 * (6 - (4 / 2)) = 10 + 2 * (6 - 2) = 10 + 2 * 4 = 10 + 8 = 18
    expected_result = 18
    actual_result = calc_resp.get("result")
    assert actual_result == expected_result, f"Incorrect math result. Expected {expected_result}, got {actual_result}."

def test_nginx_config_exists():
    filepath = "/home/user/calc-feature/nginx.conf"
    assert os.path.exists(filepath), f"Nginx configuration file {filepath} does not exist."
    assert os.path.isfile(filepath), f"Expected {filepath} to be a file."

def test_e2e_script_exists():
    filepath = "/home/user/calc-feature/run_e2e.py"
    assert os.path.exists(filepath), f"E2E script {filepath} does not exist."
    assert os.path.isfile(filepath), f"Expected {filepath} to be a file."