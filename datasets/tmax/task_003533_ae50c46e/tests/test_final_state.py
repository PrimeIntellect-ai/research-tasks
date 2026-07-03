# test_final_state.py

import os
import json
import pytest

def test_nginx_config_fixed():
    conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:8081" in content, (
        "Nginx config was not updated correctly. It should proxy traffic to 127.0.0.1:8081."
    )
    assert "8099" not in content, "The deliberate typo (8099) is still present in the Nginx config."

def test_run_job_sh_fixed():
    script_path = "/home/user/scripts/run_job.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "REPORT_DIR=/home/user/app_data" in content, "REPORT_DIR is not correctly set in run_job.sh"
    assert "TZ=UTC" in content, "TZ=UTC is not set in run_job.sh"
    assert "LC_ALL=C" in content, "LC_ALL=C is not set in run_job.sh"

def test_report_json_exists_and_valid():
    report_path = "/home/user/app_data/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} was not generated."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert "generated_at" in data, "Report JSON is missing 'generated_at' field."
    assert "UTC" in data["generated_at"], (
        f"Timestamp '{data['generated_at']}' does not contain 'UTC'. "
        "The environment variables for the job script were likely not applied correctly."
    )

def test_success_response_txt():
    response_path = "/home/user/success_response.txt"
    assert os.path.isfile(response_path), f"Success response file {response_path} is missing."

    with open(response_path, "r") as f:
        content = f.read().strip()

    assert content, f"File {response_path} is empty."

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        pytest.fail(f"File {response_path} does not contain valid JSON.")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert "data" in data, "Response JSON is missing the 'data' field."
    assert "metrics" in data["data"], "Response JSON is missing 'metrics' inside 'data'."