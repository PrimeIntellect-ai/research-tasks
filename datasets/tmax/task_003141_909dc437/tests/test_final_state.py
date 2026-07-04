# test_final_state.py

import os
import time
import json
import urllib.request
import urllib.error
import glob
import pytest
import subprocess

EVIL_CORPUS_DIR = "/app/corpus/evil"
CLEAN_CORPUS_DIR = "/app/corpus/clean"
BLOBS_DIR = "/home/user/archive/blobs"
INDEX_FILE = "/home/user/archive/master_index.jsonl"
UPLOAD_URL = "http://127.0.0.1:8080/upload"

def is_service_running(process_name: str) -> bool:
    try:
        output = subprocess.check_output(["ps", "aux"]).decode()
        return process_name in output
    except Exception:
        return False

def test_services_running():
    assert is_service_running("redis-server"), "Redis server is not running"
    assert is_service_running("nginx"), "Nginx is not running"
    assert is_service_running("intake.py") or is_service_running("flask"), "Flask API is not running"
    assert is_service_running("sanitizer.sh"), "Sanitizer worker is not running"

def test_nginx_config_updated():
    nginx_conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Nginx config not found at {nginx_conf_path}"
    with open(nginx_conf_path, "r") as f:
        content = f.read()
    assert "client_max_body_size 20m;" in content.lower() or "client_max_body_size 20M;" in content, \
        "Nginx config was not updated to allow 20M uploads."

def test_flask_api_updated():
    api_path = "/app/api/intake.py"
    assert os.path.isfile(api_path), f"Flask API file not found at {api_path}"
    with open(api_path, "r") as f:
        content = f.read()
    assert "invalid-host" not in content, "Flask API still has 'invalid-host' in redis connection string."
    assert "127.0.0.1" in content or "localhost" in content, "Flask API redis host not updated correctly."

def upload_file(filepath: str) -> str:
    with open(filepath, "rb") as f:
        data = f.read()

    req = urllib.request.Request(UPLOAD_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/octet-stream")
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode()
            try:
                return json.loads(res_body).get("uuid", "")
            except json.JSONDecodeError:
                return ""
    except urllib.error.HTTPError as e:
        return f"ERROR: {e.code}"
    except Exception as e:
        return f"ERROR: {e}"

def test_corpus_processing():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.tar"))
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.tar"))

    if not evil_files and not clean_files:
        pytest.skip("No corpus files found to process.")

    evil_uuids = {}
    clean_uuids = {}

    # Upload clean files
    for filepath in clean_files:
        uuid = upload_file(filepath)
        assert not uuid.startswith("ERROR"), f"Failed to upload clean file {filepath}: {uuid}"
        clean_uuids[filepath] = uuid

    # Upload evil files
    for filepath in evil_files:
        uuid = upload_file(filepath)
        assert not uuid.startswith("ERROR"), f"Failed to upload evil file {filepath}: {uuid}"
        evil_uuids[filepath] = uuid

    # Wait for sanitizer to process
    time.sleep(10)

    # Check clean files
    clean_failed = []
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as f:
            index_content = f.read()
    else:
        index_content = ""

    for filepath, uuid in clean_uuids.items():
        blob_path = os.path.join(BLOBS_DIR, f"{uuid}.gz")
        if not os.path.exists(blob_path):
            clean_failed.append(os.path.basename(filepath))
        # Check index
        if uuid not in index_content:
            clean_failed.append(os.path.basename(filepath) + " (missing in index)")

    # Check evil files
    evil_bypassed = []
    for filepath, uuid in evil_uuids.items():
        blob_path = os.path.join(BLOBS_DIR, f"{uuid}.gz")
        if os.path.exists(blob_path) or uuid in index_content:
            evil_bypassed.append(os.path.basename(filepath))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/missing: {', '.join(clean_failed)}")

    assert not error_msgs, " | ".join(error_msgs)