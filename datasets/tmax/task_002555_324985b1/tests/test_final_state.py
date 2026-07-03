# test_final_state.py

import os
import time
import pwd
import urllib.request

def test_user_exists():
    try:
        pwd.getpwnam("svc_backend")
    except KeyError:
        assert False, "User 'svc_backend' does not exist. The backend expects to run as this user."

def test_nginx_config_updated():
    path = "/home/user/nginx.conf"
    assert os.path.isfile(path), f"Missing Nginx configuration file at {path}"
    with open(path, "r") as f:
        content = f.read()
    assert "9090" in content, "Nginx config was not updated to forward traffic to the correct internal port (9090)."

def test_supervisor_script_exists():
    path = "/home/user/supervisor.sh"
    assert os.path.isfile(path), f"Supervisor script not found at {path}"

def test_success_rate_metric():
    success = 0
    total = 100

    for _ in range(total):
        try:
            req = urllib.request.Request("http://127.0.0.1:8080/")
            with urllib.request.urlopen(req, timeout=1) as response:
                if response.getcode() == 200:
                    success += 1
        except Exception:
            pass
        time.sleep(0.05)

    success_rate = success / total
    assert success_rate >= 0.95, f"Success rate {success_rate} is below the threshold of 0.95. Nginx and the supervisor script might not be running correctly."