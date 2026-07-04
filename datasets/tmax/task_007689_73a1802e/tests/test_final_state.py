# test_final_state.py
import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/deploy_edge.py"
ENV_DIR = "/home/user/iot_env"
NGINX_CONF = os.path.join(ENV_DIR, "nginx.conf")
LOGROTATE_CONF = os.path.join(ENV_DIR, "logrotate.conf")
MANIFEST_JSON = os.path.join(ENV_DIR, "manifest.json")

@pytest.fixture(scope="module", autouse=True)
def run_student_script():
    """Run the student's script before running the tests."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

    # Run the script once
    result1 = subprocess.run(
        ["python3", SCRIPT_PATH, "--backends", "8081,8082,8083"],
        capture_output=True, text=True
    )
    assert result1.returncode == 0, f"Script failed on first run: {result1.stderr}"

    # Run the script again to test idempotency
    result2 = subprocess.run(
        ["python3", SCRIPT_PATH, "--backends", "8081,8082,8083"],
        capture_output=True, text=True
    )
    assert result2.returncode == 0, f"Script failed on second run (idempotency check): {result2.stderr}"

def test_env_directory_exists():
    assert os.path.isdir(ENV_DIR), f"Target directory {ENV_DIR} was not created."

def test_nginx_conf():
    assert os.path.isfile(NGINX_CONF), f"Nginx config not found at {NGINX_CONF}"
    with open(NGINX_CONF, "r") as f:
        content = f.read()

    assert "upstream backend_cluster" in content, "Missing 'upstream backend_cluster' block in nginx.conf"
    assert "listen 8080" in content.replace(";", ""), "Missing 'listen 8080' in nginx.conf"
    assert "proxy_pass http://backend_cluster;" in content, "Missing 'proxy_pass http://backend_cluster;' in nginx.conf"
    assert "access_log /home/user/iot_env/access.log;" in content, "Missing 'access_log /home/user/iot_env/access.log;' in nginx.conf"

    for port in ["8081", "8082", "8083"]:
        server_line = f"server 127.0.0.1:{port};"
        assert server_line in content, f"Missing '{server_line}' in nginx.conf"
        # Check idempotency
        assert content.count(server_line) == 1, f"Duplicate '{server_line}' found in nginx.conf. Script is not idempotent."

def test_logrotate_conf():
    assert os.path.isfile(LOGROTATE_CONF), f"Logrotate config not found at {LOGROTATE_CONF}"
    with open(LOGROTATE_CONF, "r") as f:
        content = f.read()

    assert "/home/user/iot_env/access.log" in content, "Target log file not specified in logrotate.conf"
    directives = ["daily", "rotate 7", "compress", "missingok", "notifempty"]
    for directive in directives:
        assert directive in content, f"Missing directive '{directive}' in logrotate.conf"

def test_manifest_json():
    assert os.path.isfile(MANIFEST_JSON), f"Manifest JSON not found at {MANIFEST_JSON}"
    with open(MANIFEST_JSON, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("manifest.json is not valid JSON")

    assert manifest.get("status") == "success", "Manifest status should be 'success'"
    assert manifest.get("deployed_backends") == [8081, 8082, 8083], "Manifest deployed_backends does not match expected integer list"