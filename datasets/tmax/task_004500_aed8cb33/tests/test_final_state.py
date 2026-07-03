# test_final_state.py

import os
import glob
import urllib.request
import urllib.error
import subprocess
import pytest

def test_waf_script_exists():
    assert os.path.isfile("/home/user/waf.py"), "WAF script /home/user/waf.py does not exist."

def test_nginx_config_updated():
    conf_path = "/home/user/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx configuration missing at {conf_path}"

    with open(conf_path, "r") as f:
        conf = f.read()

    assert "127.0.0.1:8000" in conf, "Nginx config does not proxy to the WAF on port 8000."
    assert "/health" in conf, "Nginx config does not contain a /health location block."

def test_health_check_endpoint():
    req = urllib.request.Request("http://127.0.0.1:8080/health")
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected 200 OK for /health, got {response.status}"
            body = response.read().decode("utf-8").strip()
            assert "WAF OK" in body, f"Expected 'WAF OK' in body, got {body}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Health check failed with HTTP {e.code}")
    except urllib.error.URLError as e:
        pytest.fail(f"Health check failed to connect: {e.reason}")

def test_adversarial_corpus_filtering():
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert clean_files, f"No files found in clean corpus directory {clean_dir}"
    assert evil_files, f"No files found in evil corpus directory {evil_dir}"

    failed_clean = []
    for fpath in clean_files:
        with open(fpath, "rb") as f:
            data = f.read()
        req = urllib.request.Request("http://127.0.0.1:8080/api", data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 200:
                    failed_clean.append(os.path.basename(fpath))
        except urllib.error.HTTPError as e:
            if e.code != 200:
                failed_clean.append(os.path.basename(fpath))
        except Exception:
            failed_clean.append(os.path.basename(fpath))

    failed_evil = []
    for fpath in evil_files:
        with open(fpath, "rb") as f:
            data = f.read()
        req = urllib.request.Request("http://127.0.0.1:8080/api", data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status != 403:
                    failed_evil.append(os.path.basename(fpath))
        except urllib.error.HTTPError as e:
            if e.code != 403:
                failed_evil.append(os.path.basename(fpath))
        except Exception:
            failed_evil.append(os.path.basename(fpath))

    err_msgs = []
    if failed_clean:
        err_msgs.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean)}")
    if failed_evil:
        err_msgs.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil)}")

    if err_msgs:
        pytest.fail(" | ".join(err_msgs))

def test_storage_monitoring():
    log_file = "/home/user/waf_rejects.log"
    bash_script = "/home/user/monitor_quota.sh"
    py_script = "/home/user/monitor_quota.py"

    if os.path.exists(bash_script):
        cmd = ["bash", bash_script]
    elif os.path.exists(py_script):
        cmd = ["python3", py_script]
    else:
        pytest.fail("Monitor script not found. Expected monitor_quota.sh or monitor_quota.py")

    # Artificially pad the log file to 2048 bytes
    with open(log_file, "w") as f:
        f.write("A" * 2048)

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        assert "Quota exceeded, log truncated" in res.stdout, f"Monitor script did not print expected output. Got: {res.stdout}"
        assert os.path.getsize(log_file) == 0, f"Log file was not truncated to 0 bytes. Size is {os.path.getsize(log_file)}"
    finally:
        # Clean up
        if os.path.exists(log_file):
            os.remove(log_file)