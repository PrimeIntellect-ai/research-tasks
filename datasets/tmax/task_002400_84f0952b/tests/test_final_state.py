# test_final_state.py
import os
import subprocess
import requests
import time

def test_cron_job_exists():
    """Check that the logrotate cron job exists for the user."""
    try:
        output = subprocess.check_output(['crontab', '-l', '-u', 'user'], stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError:
        output = ""

    assert "logrotate /home/user/obs/logrotate.conf" in output, "Cron job for logrotate not found in user's crontab."
    # Check if it runs every hour (e.g., "0 * * * *")
    assert any(line.split()[1] == "*" and line.split()[2] == "*" for line in output.splitlines() if "logrotate" in line), "Cron job does not appear to be scheduled hourly."

def test_logrotate_conf():
    """Check the contents of the logrotate configuration."""
    conf_path = "/home/user/obs/logrotate.conf"
    assert os.path.exists(conf_path), f"logrotate.conf not found at {conf_path}"
    with open(conf_path, 'r') as f:
        content = f.read()

    assert "daily" in content, "logrotate.conf missing 'daily'"
    assert "rotate 3" in content, "logrotate.conf missing 'rotate 3'"
    assert "compress" in content, "logrotate.conf missing 'compress'"
    assert "copytruncate" in content, "logrotate.conf missing 'copytruncate'"

def test_start_sh_running():
    """Check that start.sh is running."""
    try:
        output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
    except subprocess.CalledProcessError:
        output = ""

    assert "start.sh" in output, "start.sh process is not running"

def test_http_endpoints():
    """Verify the metrics server endpoints."""
    base_url = "http://127.0.0.1:9090"

    # Wait briefly in case the server is just starting
    for _ in range(5):
        try:
            res = requests.get(f"{base_url}/health", timeout=2)
            if res.status_code == 200:
                break
        except requests.RequestException:
            time.sleep(1)
    else:
        assert False, "Health endpoint did not return 200 OK after retries."

    # Test /health
    res_health = requests.get(f"{base_url}/health")
    assert res_health.status_code == 200, f"/health returned {res_health.status_code}"

    # Test /metrics without auth
    res_metrics_no_auth = requests.get(f"{base_url}/metrics")
    assert res_metrics_no_auth.status_code in (401, 403), f"/metrics without auth returned {res_metrics_no_auth.status_code}"

    # Test /metrics with auth
    headers = {"Authorization": "Bearer OBS-TUNING-2024"}
    res_metrics_auth = requests.get(f"{base_url}/metrics", headers=headers)
    assert res_metrics_auth.status_code == 200, f"/metrics with auth returned {res_metrics_auth.status_code}"
    assert "critical_inode_frames_total 7" in res_metrics_auth.text, "Metrics output did not contain 'critical_inode_frames_total 7'"