# test_final_state.py

import os
import subprocess
import tempfile
import shutil
import pytest
import re

def test_nginx_configuration():
    nginx_conf_path = "/home/user/app/nginx.conf"
    assert os.path.isfile(nginx_conf_path), "nginx.conf is missing"

    with open(nginx_conf_path, "r") as f:
        content = f.read()

    # Check if proxy_pass points to port 5000
    assert re.search(r"proxy_pass\s+http://(?:127\.0\.0\.1|localhost):5000", content) or \
           re.search(r"proxy_pass\s+http://[a-zA-Z0-9_-]+:5000", content) or \
           "5000" in content, "Nginx configuration does not seem to proxy to port 5000"

def test_receiver_configuration():
    receiver_path = "/home/user/app/receiver.py"
    assert os.path.isfile(receiver_path), "receiver.py is missing"

    with open(receiver_path, "r") as f:
        content = f.read()

    assert "import redis" in content or "from redis" in content, "receiver.py does not import redis"
    assert "lpush" in content, "receiver.py does not use lpush to queue the job"

def test_sanitizer_evil_corpus():
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), "sanitizer.py is missing"

    evil_dir = "/home/user/corpora/evil"
    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.zip')]

    bypassed = []

    for evil_file in evil_files:
        zip_path = os.path.join(evil_dir, evil_file)
        with tempfile.TemporaryDirectory() as temp_out:
            result = subprocess.run(
                ["python3", sanitizer_path, zip_path, temp_out],
                capture_output=True
            )

            # Must exit with code 1 OR produce no output
            files_produced = os.listdir(temp_out)
            if result.returncode == 0 and len(files_produced) > 0:
                bypassed.append(evil_file)

    if bypassed:
        pytest.fail(f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}")

def test_sanitizer_clean_corpus():
    sanitizer_path = "/home/user/sanitizer.py"
    assert os.path.isfile(sanitizer_path), "sanitizer.py is missing"

    clean_dir = "/home/user/corpora/clean"
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.zip')]

    modified = []

    for clean_file in clean_files:
        zip_path = os.path.join(clean_dir, clean_file)
        with tempfile.TemporaryDirectory() as temp_out:
            result = subprocess.run(
                ["python3", sanitizer_path, zip_path, temp_out],
                capture_output=True
            )

            if result.returncode != 0:
                modified.append(f"{clean_file} (exit code {result.returncode})")
                continue

            # Check if output is produced
            produced_files = []
            for root, _, files in os.walk(temp_out):
                for f in files:
                    produced_files.append(os.path.join(root, f))

            if not produced_files:
                modified.append(f"{clean_file} (no output produced)")
                continue

            # Check for <script> tags and .txt files
            for fpath in produced_files:
                if fpath.endswith('.txt'):
                    modified.append(f"{clean_file} (.txt file not converted to .md)")
                    break

                with open(fpath, "r", errors="ignore") as f:
                    content = f.read()
                    if "<script>" in content:
                        modified.append(f"{clean_file} (<script> tag not stripped)")
                        break

    if modified:
        pytest.fail(f"{len(modified)} of {len(clean_files)} clean modified/failed: {', '.join(modified)}")