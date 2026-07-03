# test_final_state.py

import os
import subprocess
import pytest
import re

def test_detector_evil_corpus():
    detector_path = "/home/user/detector.py"
    assert os.path.isfile(detector_path), f"Detector script not found at {detector_path}"

    evil_dir = "/verify/corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    assert evil_files, "No JSON files found in evil corpus."

    bypassed = []
    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        res = subprocess.run(["python3", detector_path, filepath], capture_output=True)
        if res.returncode != 1:
            bypassed.append(f)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed. Offending files: {', '.join(bypassed)}")

def test_detector_clean_corpus():
    detector_path = "/home/user/detector.py"
    assert os.path.isfile(detector_path), f"Detector script not found at {detector_path}"

    clean_dir = "/verify/corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]
    assert clean_files, "No JSON files found in clean corpus."

    modified = []
    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        res = subprocess.run(["python3", detector_path, filepath], capture_output=True)
        if res.returncode != 0:
            modified.append(f)

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified. Offending files: {', '.join(modified)}")

def test_flask_config_updated():
    config_path = "/app/flask_app/config.py"
    assert os.path.isfile(config_path), f"Flask config missing at {config_path}"

    with open(config_path, 'r') as f:
        content = f.read()

    assert re.search(r'REDIS_HOST\s*=\s*["\']127\.0\.0\.1["\']', content), "REDIS_HOST not set to '127.0.0.1' in flask config."
    assert re.search(r'REDIS_PORT\s*=\s*6379', content), "REDIS_PORT not set to 6379 in flask config."

def test_nginx_config_updated():
    config_path = "/app/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config missing at {config_path}"

    with open(config_path, 'r') as f:
        content = f.read()

    assert re.search(r'proxy_pass\s+http://(127\.0\.0\.1|localhost):5000/?\s*;', content), "proxy_pass not updated to point to Flask on port 5000 in nginx config."