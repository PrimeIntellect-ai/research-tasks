# test_final_state.py
import os
import stat
import urllib.request
import concurrent.futures
import subprocess
import pytest

def fetch():
    try:
        res = urllib.request.urlopen("http://127.0.0.1:8080/ping", timeout=2)
        return 1 if res.getcode() == 200 else 0
    except Exception:
        return 0

def test_load_balancer_success_rate():
    """
    Test the metric threshold: success rate of HTTP requests to http://127.0.0.1:8080/ping >= 0.95
    """
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda _: fetch(), range(100)))

    success_rate = sum(results) / len(results)
    assert success_rate >= 0.95, f"Success rate is {success_rate}, expected >= 0.95"

def test_gunicorn_conf_fixed():
    """
    Ensure the gunicorn_conf.py file has been updated to use the BIND_SOCKET environment variable.
    """
    path = "/app/backend-api-2.1/gunicorn_conf.py"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "BIND_SOCKET" in content, f"File {path} does not use the BIND_SOCKET environment variable."

def test_sockets_exist():
    """
    Ensure that both backend instances are running and have created their respective Unix sockets.
    """
    sockets = ["/tmp/backend_1.sock", "/tmp/backend_2.sock"]
    for sock in sockets:
        assert os.path.exists(sock), f"Socket {sock} does not exist. Is the service running?"
        assert stat.S_ISSOCK(os.stat(sock).st_mode), f"Path {sock} exists but is not a socket."

def test_nginx_config_exists():
    """
    Ensure the custom Nginx configuration file exists at the required path.
    """
    path = "/home/user/nginx.conf"
    assert os.path.isfile(path), f"Nginx configuration file {path} does not exist."

def test_monitor_script_exists():
    """
    Ensure the monitoring script exists.
    """
    path = "/home/user/monitor.py"
    assert os.path.isfile(path), f"Monitoring script {path} does not exist."

def test_cron_job_exists():
    """
    Ensure a user cron job has been set up to execute the monitoring script.
    """
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        assert "monitor.py" in result.stdout, "Cron job for monitor.py not found in user crontab."
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read user crontab. Has it been set up?")