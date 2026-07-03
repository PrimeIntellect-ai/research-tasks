# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_node_code_txt():
    """Verify that the node code was extracted correctly."""
    path = "/home/user/node_code.txt"
    assert os.path.isfile(path), f"File not found: {path}"
    with open(path, "r") as f:
        content = f.read().strip().upper()
    assert content == "EPSILON-ECHO-9", f"Expected 'EPSILON-ECHO-9', got '{content}'"

def test_filter_binary_adversarial_corpus():
    """Verify the filter binary correctly classifies clean and evil corpora."""
    binary_path = "/home/user/filter"
    assert os.path.isfile(binary_path), f"Binary not found: {binary_path}"
    assert os.access(binary_path, os.X_OK), f"Binary is not executable: {binary_path}"

    clean_dir = "/app/corpora/clean/"
    evil_dir = "/app/corpora/evil/"

    clean_failed = []
    for filename in os.listdir(clean_dir):
        filepath = os.path.join(clean_dir, filename)
        if os.path.isfile(filepath):
            result = subprocess.run([binary_path, filepath], capture_output=True)
            if result.returncode != 0:
                clean_failed.append(filename)

    evil_failed = []
    for filename in os.listdir(evil_dir):
        filepath = os.path.join(evil_dir, filename)
        if os.path.isfile(filepath):
            result = subprocess.run([binary_path, filepath], capture_output=True)
            if result.returncode != 1:
                evil_failed.append(filename)

    error_messages = []
    if clean_failed:
        error_messages.append(f"{len(clean_failed)} clean files modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        error_messages.append(f"{len(evil_failed)} evil files bypassed/accepted: {', '.join(evil_failed)}")

    assert not error_messages, "Adversarial corpus verification failed: " + "; ".join(error_messages)

def test_pipeline_and_dirs():
    """Verify pipeline script and required directories exist."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

    for d in ["/home/user/incoming", "/home/user/approved", "/home/user/rejected"]:
        assert os.path.isdir(d), f"Directory not found: {d}"

def test_cron_job():
    """Verify the cron job is set up correctly."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run crontab -l"

    cron_lines = result.stdout.strip().split('\n')
    expected_job = "* * * * * /home/user/pipeline.sh"

    found = any(expected_job in line for line in cron_lines if not line.strip().startswith('#'))
    assert found, f"Cron job '{expected_job}' not found in crontab"

def test_nginx_config_and_running():
    """Verify Nginx configuration and that it is serving on port 8080."""
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config not found: {conf_path}"

    with open(conf_path, "r") as f:
        conf_content = f.read()

    assert "root /home/user/approved" in conf_content or "root /home/user/approved/" in conf_content, \
        "Nginx config does not define root as /home/user/approved/"

    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=2) as response:
            status = response.getcode()
            assert status in [200, 403], f"Unexpected status code {status}"
    except urllib.error.HTTPError as e:
        assert e.code in [200, 403], f"Unexpected HTTP error code {e.code}"
    except Exception as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")