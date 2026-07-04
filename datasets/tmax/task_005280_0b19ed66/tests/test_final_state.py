# test_final_state.py

import os
import stat
import pytest

def test_nginx_conf_updated():
    conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"File missing: {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    assert "proxy_pass http://unix:/home/user/run/health_monitor.sock;" in content, \
        "nginx.conf does not contain the corrected proxy_pass directive pointing to health_monitor.sock."

def test_health_check_log_contains_status():
    log_path = "/home/user/logs/health_check.log"
    assert os.path.isfile(log_path), f"Health check log missing: {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert "STATUS: UP" in content, \
        f"{log_path} does not contain 'STATUS: UP'. The C service might not be returning the correct fixed HTTP response."

def test_alerts_mbox_contains_alert():
    mbox_path = "/home/user/mail/alerts.mbox"
    assert os.path.isfile(mbox_path), f"Alerts mbox missing: {mbox_path}"

    with open(mbox_path, "r") as f:
        content = f.read()

    assert "ALERT: Service degraded" in content, \
        f"{mbox_path} does not contain 'ALERT: Service degraded'. The C service alert logic or curl command might be failing."

def test_deploy_script_exists_and_executable():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script missing: {script_path}"

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deploy script {script_path} is not executable."