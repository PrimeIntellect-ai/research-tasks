# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import concurrent.futures
import pytest

def test_nginx_config_fixed():
    nginx_conf_path = "/home/user/app/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Missing {nginx_conf_path}"

    with open(nginx_conf_path, "r") as f:
        content = f.read()

    # Nginx should proxy to port 5000 instead of 5001
    assert "5000" in content and "5001" not in content, "Nginx config was not correctly updated to proxy to port 5000."

def test_backend_env_fixed():
    env_path = "/home/user/app/backend/.env"
    assert os.path.isfile(env_path), f"Missing {env_path}"

    with open(env_path, "r") as f:
        content = f.read()

    assert "redis://127.0.0.1:6379/0" in content or "redis://localhost:6379/0" in content, "Redis URL in .env not correctly configured to redis://127.0.0.1:6379/0."

def test_concurrency_no_deadlock():
    # Send concurrent requests to ensure the Flask deadlock is resolved
    def fetch():
        req = urllib.request.Request("http://127.0.0.1:8080/process", data=b"test_payload", method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status
        except urllib.error.URLError as e:
            if hasattr(e, 'code'):
                return e.code
            return None
        except Exception:
            return None

    results = []
    # 10 workers sending 20 requests should easily trigger a deadlock if not fixed
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(fetch) for _ in range(20)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())

    failed = [r for r in results if r != 200]
    assert not failed, f"Concurrency test failed: {len(failed)} out of 20 requests did not return HTTP 200. The deadlock may still exist or services are not properly connected."

def test_detector_adversarial_corpus():
    detector_script = "/home/user/app/detector.py"
    assert os.path.isfile(detector_script), f"Detector script missing at {detector_script}"

    evil_dir = "/home/user/app/corpora/evil/"
    clean_dir = "/home/user/app/corpora/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No files found in evil corpus."
    assert len(clean_files) > 0, "No files found in clean corpus."

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run(["python3", detector_script, f], capture_output=True, text=True)
        # Evil files must exit with 1 and print EVIL
        if res.returncode != 1 or "EVIL" not in res.stdout:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        res = subprocess.run(["python3", detector_script, f], capture_output=True, text=True)
        # Clean files must exit with 0 and print CLEAN
        if res.returncode != 0 or "CLEAN" not in res.stdout:
            clean_modified.append(os.path.basename(f))

    err_msg = []
    if evil_bypassed:
        err_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        err_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    assert not err_msg, " | ".join(err_msg)