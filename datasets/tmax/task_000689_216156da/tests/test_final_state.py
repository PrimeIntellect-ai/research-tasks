# test_final_state.py

import os
import subprocess
import pytest
import urllib.request
import time

def test_start_env_script_exists():
    """Check that the startup script exists and is executable."""
    script_path = "/home/user/start_env.sh"
    assert os.path.isfile(script_path), f"Startup script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Startup script {script_path} is not executable."

def test_nginx_config_csp_and_proxy():
    """Verify Nginx configuration contains the required CSP and proxy settings."""
    nginx_conf_path = "/app/target_env/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Nginx config {nginx_conf_path} does not exist."

    with open(nginx_conf_path, 'r') as f:
        content = f.read()

    assert "proxy_pass http://127.0.0.1:5000" in content or "proxy_pass http://localhost:5000" in content, \
        "Nginx config does not proxy traffic to the Flask app on port 5000."
    assert "listen 8080" in content, "Nginx config does not listen on port 8080."

    csp_directive = "Content-Security-Policy"
    assert csp_directive in content, "Nginx config is missing the Content-Security-Policy header."
    assert "script-src 'self'" in content, "CSP does not restrict script-src to 'self'."
    assert "object-src 'self'" in content, "CSP does not restrict object-src to 'self'."

def test_waf_mock_adversarial_corpus():
    """
    Test the WAF mock script against the clean and evil corpora.
    The script must output CLEAN for all clean URLs and EVIL for all evil URLs.
    """
    waf_script = "/home/user/waf_mock.py"
    clean_corpus = "/app/corpora/clean_urls.txt"
    evil_corpus = "/app/corpora/evil_payloads.txt"

    assert os.path.isfile(waf_script), f"WAF mock script {waf_script} does not exist."
    assert os.path.isfile(clean_corpus), f"Clean corpus {clean_corpus} does not exist."
    assert os.path.isfile(evil_corpus), f"Evil corpus {evil_corpus} does not exist."

    with open(clean_corpus, 'r') as f:
        clean_urls = [line.strip() for line in f if line.strip()]

    with open(evil_corpus, 'r') as f:
        evil_urls = [line.strip() for line in f if line.strip()]

    # Test Clean URLs
    clean_bypassed = []
    for url in clean_urls:
        process = subprocess.Popen(
            ["python3", waf_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, _ = process.communicate(input=url + "\n")
        output = stdout.strip()
        if output != "CLEAN":
            clean_bypassed.append(url)

    # Test Evil URLs
    evil_bypassed = []
    for url in evil_urls:
        process = subprocess.Popen(
            ["python3", waf_script],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, _ = process.communicate(input=url + "\n")
        output = stdout.strip()
        if output != "EVIL":
            evil_bypassed.append(url)

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_urls)} evil bypassed. Offending URLs: {', '.join(evil_bypassed[:5])}...")
    if clean_bypassed:
        error_messages.append(f"{len(clean_bypassed)} of {len(clean_urls)} clean modified/rejected. Offending URLs: {', '.join(clean_bypassed[:5])}...")

    if error_messages:
        pytest.fail(" | ".join(error_messages))