# test_final_state.py

import os
import json
import subprocess
import pytest

def test_tls_certificates_exist():
    cert_path = "/app/nginx/ssl/cert.pem"
    key_path = "/app/nginx/ssl/key.pem"
    assert os.path.isfile(cert_path), f"TLS certificate missing: {cert_path}"
    assert os.path.isfile(key_path), f"TLS private key missing: {key_path}"
    assert os.path.getsize(cert_path) > 0, f"TLS certificate is empty: {cert_path}"
    assert os.path.getsize(key_path) > 0, f"TLS private key is empty: {key_path}"

def test_nginx_proxy_configuration():
    conf_path = "/app/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config missing: {conf_path}"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "http://127.0.0.1:5000" in content, "Nginx config does not proxy to the correct Flask port (5000)."

def test_attacker_ip_extracted():
    ip_path = "/home/user/attacker_ip.txt"
    assert os.path.isfile(ip_path), f"Attacker IP file missing: {ip_path}"
    with open(ip_path, "r") as f:
        ip = f.read().strip()
    assert ip == "10.13.37.99", f"Incorrect attacker IP extracted. Expected '10.13.37.99', got '{ip}'"

def test_jwt_filter_adversarial_corpus():
    script_path = "/home/user/jwt_filter.py"
    assert os.path.isfile(script_path), f"JWT filter script missing: {script_path}"

    clean_dir = "/app/corpora/clean"
    evil_dir = "/app/corpora/evil"
    clean_out = "/tmp/clean_out.json"
    evil_out = "/tmp/evil_out.json"

    # Run on clean corpus
    subprocess.run(["python3", script_path, clean_dir, clean_out], check=False)
    # Run on evil corpus
    subprocess.run(["python3", script_path, evil_dir, evil_out], check=False)

    assert os.path.isfile(clean_out), f"Output JSON for clean corpus missing: {clean_out}"
    assert os.path.isfile(evil_out), f"Output JSON for evil corpus missing: {evil_out}"

    with open(clean_out, "r") as f:
        clean_results = json.load(f)
    with open(evil_out, "r") as f:
        evil_results = json.load(f)

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for cf in clean_files:
        if not clean_results.get(cf, False):
            clean_failed.append(cf)

    evil_bypassed = []
    for ef in evil_files:
        if evil_results.get(ef, True):
            evil_bypassed.append(ef)

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, "JWT Filter failed corpus validation:\n" + "\n".join(errors)