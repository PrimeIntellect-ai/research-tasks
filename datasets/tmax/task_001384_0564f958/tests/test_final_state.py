# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_success_file():
    success_file = "/home/user/success.txt"
    assert os.path.isfile(success_file), f"The file {success_file} was not created."

    with open(success_file, "r") as f:
        content = f.read().strip()

    assert content == '{"status": "ok"}', f"Expected success.txt to contain '{{\"status\": \"ok\"}}', but got '{content}'."

def test_nginx_proxy_works():
    url = "http://127.0.0.1:8080/api/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status_code = response.getcode()
            body = response.read().decode("utf-8").strip()

        assert status_code == 200, f"Expected HTTP 200 OK, got {status_code}"
        assert body == '{"status": "ok"}', f"Expected response body '{{\"status\": \"ok\"}}', got '{body}'"
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTP error occurred while accessing {url}: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url}: {e.reason}")
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {e}")

def test_supervisor_process_running():
    cmd = ["supervisorctl", "-c", "/home/user/supervisor/supervisord.conf", "status", "backend-api"]
    try:
        output = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT)
        assert "RUNNING" in output, f"Expected backend-api to be RUNNING, but got status output:\n{output}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"supervisorctl command failed with exit code {e.returncode} and output:\n{e.output}")

def test_deploy_sh_updated():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"The file {deploy_script} is missing."

    with open(deploy_script, "r") as f:
        content = f.read()

    assert "supervisorctl" in content, "The deploy.sh script does not contain a 'supervisorctl' command."