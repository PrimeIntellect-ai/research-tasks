# test_final_state.py
import os
import re
import subprocess
import pytest

def test_nginx_config_updated():
    path = "/home/user/nginx.conf"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check for proxy_pass http://127.0.0.1:8453;
    # Allow some whitespace variations
    match = re.search(r"proxy_pass\s+http://127\.0\.0\.1:8453\s*;", content)
    assert match is not None, "nginx.conf does not contain 'proxy_pass http://127.0.0.1:8453;'"

def test_waf_executable_exists():
    path = "/home/user/waf"
    assert os.path.exists(path), f"WAF executable {path} does not exist."
    assert os.access(path, os.X_OK), f"WAF executable {path} is not executable."

def test_waf_corpus_checks():
    waf_path = "/home/user/waf"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    assert os.path.exists(waf_path), f"WAF executable {waf_path} missing."
    assert os.path.exists(clean_dir), f"Clean corpus {clean_dir} missing."
    assert os.path.exists(evil_dir), f"Evil corpus {evil_dir} missing."

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for fpath in clean_files:
        result = subprocess.run([waf_path, fpath], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(fpath))

    evil_failed = []
    for fpath in evil_files:
        result = subprocess.run([waf_path, fpath], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(os.path.basename(fpath))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")

    assert not errors, "WAF corpus checks failed: " + "; ".join(errors)