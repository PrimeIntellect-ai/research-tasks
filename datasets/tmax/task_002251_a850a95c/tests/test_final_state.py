# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import subprocess
import pytest

def test_deployment_health():
    """Verify that Nginx, Flask, and Redis are correctly wired up and healthy."""
    url = "http://127.0.0.1:8080/api/health"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
            assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"
            assert data.get("redis") == "connected", f"Expected redis 'connected', got {data.get('redis')}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to {url}: {e}")
    except json.JSONDecodeError:
        pytest.fail("Response from health endpoint was not valid JSON.")

def test_symlink_updated():
    """Verify the symlink points to v2."""
    current_link = "/home/user/deploy/current"
    assert os.path.islink(current_link), f"{current_link} is not a symlink."
    target = os.readlink(current_link)
    assert target.endswith("v2") or target == "/home/user/deploy/v2", f"Symlink points to {target}, expected /home/user/deploy/v2"

def test_start_script_env_var():
    """Verify the start script exports REDIS_HOST."""
    start_script = "/home/user/deploy/current/start.sh"
    assert os.path.isfile(start_script), f"Start script {start_script} not found."
    with open(start_script, "r") as f:
        content = f.read()
    assert "REDIS_HOST=127.0.0.1" in content or "export REDIS_HOST" in content, "REDIS_HOST environment variable is not exported in start.sh"

def test_waf_detector_corpus():
    """Verify the WAF detector against the hidden adversarial corpus."""
    script_path = "/home/user/waf_detector.py"
    assert os.path.isfile(script_path), f"WAF detector script {script_path} not found."

    evil_dir = "/home/user/corpora_hidden/evil"
    clean_dir = "/home/user/corpora_hidden/clean"

    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} missing."
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} missing."

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    for filepath in evil_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "EVIL":
            evil_bypassed.append((os.path.basename(filepath), output))

    clean_modified = []
    for filepath in clean_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "CLEAN":
            clean_modified.append((os.path.basename(filepath), output))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: " + ", ".join([f"{f} (output: {o})" for f, o in evil_bypassed]))
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/flagged. Offending files: " + ", ".join([f"{f} (output: {o})" for f, o in clean_modified]))

    if errors:
        pytest.fail(" | ".join(errors))

def test_monitor_logs_script_and_cron():
    """Verify the log monitoring script and cron job."""
    script_path = "/home/user/monitor_logs.sh"
    assert os.path.isfile(script_path), f"Log monitoring script {script_path} not found."
    assert os.access(script_path, os.X_OK), f"Log monitoring script {script_path} is not executable."

    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."

    crontab_content = result.stdout
    assert "monitor_logs.sh" in crontab_content, "monitor_logs.sh not found in crontab."
    assert "*/5" in crontab_content, "Cron job is not scheduled to run every 5 minutes (missing '*/5')."
    assert "suspicious_ips.txt" in crontab_content, "Cron job output is not appended to suspicious_ips.txt."