# test_final_state.py

import os
import subprocess
import pytest

def test_classifier_corpus():
    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"
    classifier_path = "/home/user/classifier.py"

    assert os.path.isfile(classifier_path), f"Classifier script missing at {classifier_path}"

    # Test EVIL corpus
    res_evil = subprocess.run(["python3", classifier_path, evil_dir], capture_output=True, text=True)
    evil_output = res_evil.stdout.strip().split('\n')
    evil_results = {}
    for line in evil_output:
        if ":" in line:
            fname, label = line.split(":", 1)
            evil_results[fname.strip()] = label.strip()

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.log')]
    evil_bypassed = []
    for f in evil_files:
        if evil_results.get(f) != "EVIL":
            evil_bypassed.append(f)

    # Test CLEAN corpus
    res_clean = subprocess.run(["python3", classifier_path, clean_dir], capture_output=True, text=True)
    clean_output = res_clean.stdout.strip().split('\n')
    clean_results = {}
    for line in clean_output:
        if ":" in line:
            fname, label = line.split(":", 1)
            clean_results[fname.strip()] = label.strip()

    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.log')]
    clean_modified = []
    for f in clean_files:
        if clean_results.get(f) != "CLEAN":
            clean_modified.append(f)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)

def test_nginx_config_fixed():
    nginx_conf_path = "/app/audit_pipeline/config/nginx.conf"
    assert os.path.isfile(nginx_conf_path), "Nginx config file missing"
    with open(nginx_conf_path, "r") as f:
        content = f.read()

    # Nginx should not hide the Cookie header anymore
    assert "proxy_hide_header Cookie;" not in content or "proxy_pass_header Cookie;" in content, \
        "Nginx is still configured to drop the Cookie header."

def test_flask_api_fixed():
    api_path = "/app/audit_pipeline/api.py"
    assert os.path.isfile(api_path), "Flask API file missing"
    with open(api_path, "r") as f:
        content = f.read()

    assert "port=6380" not in content, "Flask API is still connecting to the broken Redis port (6380)."
    assert "6379" in content, "Flask API does not appear to connect to the correct Redis port (6379)."

def test_worker_fixed():
    worker_path = "/app/audit_pipeline/worker.py"
    assert os.path.isfile(worker_path), "Worker script missing"
    with open(worker_path, "r") as f:
        content = f.read()

    assert "--cred" not in content, "Worker is still passing credentials via the '--cred' command-line argument."
    assert "--read-stdin" in content, "Worker is not passing the '--read-stdin' flag to the logger."
    assert "input=" in content or "stdin=" in content or "communicate" in content, \
        "Worker does not appear to pipe the decrypted credential to stdin."