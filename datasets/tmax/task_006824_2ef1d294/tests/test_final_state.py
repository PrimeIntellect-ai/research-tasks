# test_final_state.py
import os
import urllib.request
import urllib.error
import pytest

def test_symlink_updated():
    symlink_path = "/home/user/deploy/current"
    assert os.path.islink(symlink_path), f"Symlink {symlink_path} is missing."
    target = os.readlink(symlink_path)
    assert target == "/home/user/deploy/v2", f"Symlink {symlink_path} points to {target}, expected /home/user/deploy/v2."

def test_service_running():
    url = "http://127.0.0.1:8080/status"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode('utf-8').strip()
            assert body == "OK-v2", f"Expected response 'OK-v2', got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to service at {url}: {e}")

def test_email_file():
    email_path = "/home/user/mail/new/deployment_report.eml"
    assert os.path.isfile(email_path), f"Email file {email_path} is missing."

    with open(email_path, 'r') as f:
        content = f.read()

    assert "To: team@local" in content, "Email is missing 'To: team@local'"
    assert "From: deploy@local" in content, "Email is missing 'From: deploy@local'"
    assert "Subject: Deployment Success" in content, "Email is missing 'Subject: Deployment Success'"
    assert "Service v2 is live." in content, "Email is missing the required body text 'Service v2 is live.'"

def test_scripts_exist():
    expect_script = "/home/user/scripts/start_service.exp"
    deploy_script = "/home/user/scripts/deploy.sh"

    assert os.path.isfile(expect_script), f"Expect script {expect_script} is missing."
    assert os.path.isfile(deploy_script), f"Deploy script {deploy_script} is missing."

def test_v2_app_exists():
    app_path = "/home/user/deploy/v2/app"
    assert os.path.isfile(app_path), f"v2 app {app_path} is missing."
    assert os.access(app_path, os.X_OK), f"v2 app {app_path} is not executable."