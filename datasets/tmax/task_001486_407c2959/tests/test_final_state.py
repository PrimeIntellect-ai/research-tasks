# test_final_state.py

import os
import glob
import subprocess
import tempfile
import tarfile
import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import json

def test_sanitizer_executable():
    script_path = "/home/user/pipeline/sanitizer.sh"
    assert os.path.isfile(script_path), f"Sanitizer script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Sanitizer script {script_path} is not executable"

def test_evil_corpus_rejected():
    script_path = "/home/user/pipeline/sanitizer.sh"
    evil_files = glob.glob("/home/user/corpora/evil/*.tar.gz")
    assert evil_files, "No evil corpus files found"

    bypassed = []
    for evil_file in evil_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run([script_path, evil_file, tmpdir], capture_output=True, text=True)
            if result.returncode == 0:
                bypassed.append(os.path.basename(evil_file))

    assert not bypassed, f"{len(bypassed)} of {len(evil_files)} evil bypassed: {', '.join(bypassed)}"

def test_clean_corpus_accepted_and_transformed():
    script_path = "/home/user/pipeline/sanitizer.sh"
    clean_files = glob.glob("/home/user/corpora/clean/*.tar.gz")
    assert clean_files, "No clean corpus files found"

    modified_or_failed = []
    for clean_file in clean_files:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run([script_path, clean_file, tmpdir], capture_output=True, text=True)
            if result.returncode != 0:
                modified_or_failed.append(f"{os.path.basename(clean_file)} (rejected)")
                continue

            out_tar = os.path.join(tmpdir, "sanitized_bundle.tar.gz")
            if not os.path.isfile(out_tar):
                modified_or_failed.append(f"{os.path.basename(clean_file)} (missing output tar)")
                continue

            with tarfile.open(out_tar, "r:gz") as tar:
                names = tar.getnames()
                has_xml = any(name.endswith("app_config.xml") for name in names)
                has_json = any(name.endswith("app_config.json") for name in names)

                if has_json or not has_xml:
                    modified_or_failed.append(f"{os.path.basename(clean_file)} (json not converted to xml properly)")

    assert not modified_or_failed, f"{len(modified_or_failed)} of {len(clean_files)} clean failed/modified: {', '.join(modified_or_failed)}"

def test_end_to_end_flow():
    # We will upload a clean tar to nginx, check if it proxies to flask, runs sanitizer, and writes to redis
    clean_files = glob.glob("/home/user/corpora/clean/*.tar.gz")
    assert clean_files, "No clean corpus files found for end-to-end test"

    test_file = clean_files[0]

    # Use curl to upload
    curl_cmd = [
        "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
        "-F", f"file=@{test_file}",
        "http://127.0.0.1:8080/upload"
    ]

    result = subprocess.run(curl_cmd, capture_output=True, text=True)
    assert result.stdout.strip() in ["200", "201"], f"Upload to Nginx failed, HTTP code: {result.stdout}"

    # Check redis
    redis_cmd = ["redis-cli", "get", "config_status"]
    redis_result = subprocess.run(redis_cmd, capture_output=True, text=True)

    assert "SECURE_UPDATE_APPLIED" in redis_result.stdout, "Redis key config_status does not have SECURE_UPDATE_APPLIED"