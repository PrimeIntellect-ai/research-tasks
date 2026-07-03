# test_final_state.py
import os
import json
import urllib.request
import urllib.error
import pytest

def test_fetch_costs_exp_exists():
    path = "/home/user/fetch_costs.exp"
    assert os.path.isfile(path), f"Expect script {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "expect" in content, f"File {path} does not seem to contain expect commands."

def test_deploy_sh_exists_and_executable():
    path = "/home/user/deploy.sh"
    assert os.path.isfile(path), f"Deployment script {path} does not exist."
    assert os.access(path, os.X_OK), f"Deployment script {path} is not executable."

def test_staging_report_json():
    path = "/home/user/staging/report.json"
    assert os.path.isfile(path), f"Staging report {path} does not exist."
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    assert data.get("total_cost") == 4250.75, f"Staging report total_cost is incorrect."
    assert data.get("status") == "success", f"Staging report status is incorrect."

def test_prod_report_json():
    staging_path = "/home/user/staging/report.json"
    prod_path = "/home/user/prod/report.json"
    assert os.path.isfile(prod_path), f"Production report {prod_path} does not exist."

    with open(staging_path, "r") as f:
        staging_data = f.read()
    with open(prod_path, "r") as f:
        prod_data = f.read()

    assert staging_data == prod_data, f"Production report does not match staging report."

def test_web_server_running():
    url = "http://localhost:8080/report.json"
    try:
        response = urllib.request.urlopen(url, timeout=2)
        assert response.status == 200, f"Web server returned status {response.status} instead of 200."
        data = json.loads(response.read().decode('utf-8'))
        assert data.get("total_cost") == 4250.75, "Web server did not serve the correct report.json."
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to web server on port 8080: {e}")
    except json.JSONDecodeError:
        pytest.fail(f"Web server did not return valid JSON.")

def test_email_notification_sent():
    log_path = "/home/user/mail.log"
    assert os.path.isfile(log_path), f"Mail log {log_path} does not exist. Was the email sent?"

    with open(log_path, "r") as f:
        log_content = f.read()

    assert "finops@localhost" in log_content, "Sender finops@localhost not found in mail log."
    assert "cfo@example.com" in log_content, "Recipient cfo@example.com not found in mail log."
    assert "Cost Report Deployed" in log_content, "Subject 'Cost Report Deployed' not found in mail log."
    assert "The latest cost report has been deployed to the web server." in log_content, "Expected email body not found in mail log."