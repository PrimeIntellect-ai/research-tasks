# test_final_state.py

import os
import subprocess

def test_auto_deploy_exp_exists():
    exp_path = "/home/user/auto_deploy.exp"
    assert os.path.isfile(exp_path), f"The expect script {exp_path} is missing."

def test_python_backend_running():
    try:
        # Check if the python backend app is running
        output = subprocess.check_output(["pgrep", "-f", "app.py"]).decode("utf-8")
        assert output.strip() != "", "The Python backend (app.py) process is not running."
    except subprocess.CalledProcessError:
        assert False, "The Python backend (app.py) process is not running."

def test_nginx_config_fixed():
    config_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config file {config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read()
        # The backend runs on 9001, so proxy_pass should point to it
        assert "127.0.0.1:9001" in content or "localhost:9001" in content, \
            f"Nginx config {config_path} does not correctly route to the backend on port 9001."

def test_resolution_log():
    log_path = "/home/user/resolution.log"
    assert os.path.isfile(log_path), f"The resolution log file {log_path} is missing."
    with open(log_path, "r") as f:
        content = f.read().strip()
        expected = "Hello from Production backend!"
        assert content == expected, f"Content of {log_path} does not match expected output. Got: {content}"