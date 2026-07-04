# test_final_state.py
import os
import urllib.request
import urllib.error

def test_nginx_config_fixed():
    """Verify that the Nginx configuration points to the correct socket."""
    conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx configuration missing at {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "server unix:/home/user/app/backend.sock;" in content, \
        "Nginx configuration does not have the correct upstream socket path (/home/user/app/backend.sock)."

def test_deploy_status_log():
    """Verify the deployment script created the correct log file with the expected contents."""
    log_path = "/home/user/deploy_status.log"
    assert os.path.isfile(log_path), f"Deployment log missing at {log_path}"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "DEPLOYMENT_SUCCESS: 200 OK", \
        f"Deployment log content is incorrect. Expected 'DEPLOYMENT_SUCCESS: 200 OK', got '{content}'."

def test_health_endpoint():
    """Verify that the Nginx server and backend are running and responding correctly."""
    url = "http://127.0.0.1:8080/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode('utf-8').strip()

            assert status == 200, f"Expected HTTP 200 OK, got {status}."
            assert body == "OK", f"Expected body 'OK', got '{body}'."
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx at {url}: {e}"