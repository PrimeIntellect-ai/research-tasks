# test_final_state.py

import os
import subprocess
import pytest
import re

def test_scanner_clean_corpus():
    scanner_path = "/home/user/scanner.py"
    assert os.path.isfile(scanner_path), f"{scanner_path} is missing"

    clean_dir = "/app/corpora/clean"
    assert os.path.isdir(clean_dir), f"{clean_dir} is missing"

    files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert len(files) > 0, f"No files found in {clean_dir}"

    failed_files = []
    for filename in files:
        filepath = os.path.join(clean_dir, filename)
        result = subprocess.run(["python3", scanner_path, filepath], capture_output=True, text=True)
        if result.returncode != 0 or "CLEAN" not in result.stdout:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(files)} clean files modified/rejected: {', '.join(failed_files)}"

def test_scanner_evil_corpus():
    scanner_path = "/home/user/scanner.py"
    assert os.path.isfile(scanner_path), f"{scanner_path} is missing"

    evil_dir = "/app/corpora/evil"
    assert os.path.isdir(evil_dir), f"{evil_dir} is missing"

    files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert len(files) > 0, f"No files found in {evil_dir}"

    failed_files = []
    for filename in files:
        filepath = os.path.join(evil_dir, filename)
        result = subprocess.run(["python3", scanner_path, filepath], capture_output=True, text=True)
        if result.returncode != 1 or "EVIL" not in result.stdout:
            failed_files.append(filename)

    assert not failed_files, f"{len(failed_files)} of {len(files)} evil files bypassed: {', '.join(failed_files)}"

def test_nginx_config_validity_and_content():
    nginx_conf = "/home/user/nginx.conf"
    assert os.path.isfile(nginx_conf), f"{nginx_conf} is missing"

    with open(nginx_conf, 'r') as f:
        content = f.read()

    # Check listen port
    assert re.search(r'listen\s+8080\b', content), "Nginx config does not listen on port 8080"

    # Check proxy_pass
    assert re.search(r'proxy_pass\s+http://127\.0\.0\.1:9000\b', content), "Nginx config does not proxy to http://127.0.0.1:9000"

    # Check rate limit zone
    assert re.search(r'limit_req_zone\s+.*zone=upload_limit:10m\s+rate=10r/s\b', content), "Nginx config does not define the correct limit_req_zone"