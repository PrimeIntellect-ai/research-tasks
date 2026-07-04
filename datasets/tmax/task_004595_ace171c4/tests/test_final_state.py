# test_final_state.py

import os
import stat
import json
import urllib.request

def test_nginx_config_updated():
    config_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx configuration {config_path} is missing."

    with open(config_path, "r") as f:
        content = f.read()

    assert "server unix:/home/user/app.sock;" in content, "Nginx config was not updated to point to unix:/home/user/app.sock."
    assert "server unix:/tmp/legacy.sock;" not in content, "Nginx config still contains the legacy socket path."

def test_manage_service_script_exists_and_executable():
    script_path = "/home/user/manage_service.sh"
    assert os.path.isfile(script_path), f"Service manager script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Service manager script {script_path} is not executable."

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deployment script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deployment script {script_path} is not executable."

def test_migration_log_contains_success_message():
    log_path = "/home/user/migration.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did you execute deploy.sh?"

    with open(log_path, "r") as f:
        content = f.read()

    assert "Migration Complete" in content, f"Log file {log_path} does not contain the expected success message."

def test_services_are_running_and_accessible():
    sock_path = "/home/user/app.sock"
    assert os.path.exists(sock_path), f"Socket {sock_path} is missing. The backend service may not be running."

    pid_path = "/home/user/app.pid"
    assert os.path.isfile(pid_path), f"PID file {pid_path} is missing. The backend service may not have been started correctly."

    try:
        req = urllib.request.Request("http://localhost:8080/api")
        with urllib.request.urlopen(req, timeout=3) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode())
            assert data.get("status") == "ok", "API did not return status: ok"
            assert data.get("message") == "Migration Complete", "API did not return the expected message"
    except Exception as e:
        assert False, f"Failed to access the API via Nginx at http://localhost:8080/api. Error: {e}"