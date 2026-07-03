# test_final_state.py

import os
import re
import subprocess
import pytest

def test_dnsmasq_config():
    conf_path = "/home/user/sandbox/dnsmasq.conf"
    assert os.path.exists(conf_path), f"Missing {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    # Check for the address resolution directive
    assert re.search(r"address=/c2-malware\.local/127\.0\.0\.1", content), \
        "dnsmasq.conf does not correctly resolve c2-malware.local to 127.0.0.1"

def test_nginx_config():
    conf_path = "/home/user/sandbox/nginx.conf"
    assert os.path.exists(conf_path), f"Missing {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    # Check for listen directive on port 8080
    assert re.search(r"listen\s+8080", content), \
        "nginx.conf does not contain a listen directive for port 8080"

    # Check for proxy_pass to the flask sinkhole
    assert re.search(r"proxy_pass\s+http://127\.0\.0\.1:5000", content), \
        "nginx.conf does not contain a proxy_pass directive to http://127.0.0.1:5000"

def test_parser_fixed_exists_and_executable():
    parser_path = "/home/user/evidence/parser_fixed"
    assert os.path.exists(parser_path), f"Fixed parser binary missing at {parser_path}"
    assert os.access(parser_path, os.X_OK), f"Fixed parser at {parser_path} is not executable"

def test_classifier_accuracy():
    classifier_path = "/home/user/classifier.py"
    assert os.path.exists(classifier_path), f"Classifier script missing at {classifier_path}"

    evil_dir = "/app/verifier/corpus/evil"
    clean_dir = "/app/verifier/corpus/clean"

    assert os.path.exists(evil_dir), f"Evil corpus missing at {evil_dir}"
    assert os.path.exists(clean_dir), f"Clean corpus missing at {clean_dir}"

    evil_files = os.listdir(evil_dir)
    clean_files = os.listdir(clean_dir)

    evil_failed = []
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        res = subprocess.run(["python3", classifier_path, path], capture_output=True, text=True)
        if res.stdout.strip() != "EVIL":
            evil_failed.append(f)

    clean_failed = []
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        res = subprocess.run(["python3", classifier_path, path], capture_output=True, text=True)
        if res.stdout.strip() != "CLEAN":
            clean_failed.append(f)

    assert not evil_failed, f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {evil_failed[:5]}"
    assert not clean_failed, f"{len(clean_failed)} of {len(clean_files)} clean modified (flagged incorrectly): {clean_failed[:5]}"