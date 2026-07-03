# test_final_state.py

import os
import subprocess
import pytest
import re

def test_waf_classifier_corpus():
    """Test the WAF classifier against the clean and evil corpora."""
    classifier_path = "/home/user/waf_classifier.py"
    assert os.path.isfile(classifier_path), f"WAF classifier script not found at {classifier_path}"

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No files found in clean corpus."
    assert len(evil_files) > 0, "No files found in evil corpus."

    clean_failures = []
    for clean_file in clean_files:
        result = subprocess.run(
            ["python3", classifier_path, clean_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "ACCEPT":
            clean_failures.append(os.path.basename(clean_file))

    evil_failures = []
    for evil_file in evil_files:
        result = subprocess.run(
            ["python3", classifier_path, evil_file],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "REJECT":
            evil_failures.append(os.path.basename(evil_file))

    error_messages = []
    if evil_failures:
        error_messages.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_messages.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    assert not error_messages, "WAF classifier failed corpus tests:\n" + "\n".join(error_messages)

def test_nginx_config_contents():
    """Test that nginx.conf is correctly generated with required directives."""
    config_path = "/home/user/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config not found at {config_path}"

    with open(config_path, "r") as f:
        config_content = f.read()

    # Check for port 8443
    assert re.search(r"listen\s+8443\s+ssl", config_content) or re.search(r"listen\s+8443", config_content), \
        "Nginx config does not listen on port 8443 (HTTPS)."

    # Check for TLS certs
    assert "/app/certs/server.crt" in config_content, "Nginx config missing server.crt path."
    assert "/app/certs/server.key" in config_content, "Nginx config missing server.key path."

    # Check for proxy_pass to upstream 9090
    assert re.search(r"proxy_pass\s+http://(?:127\.0\.0\.1|localhost):9090", config_content), \
        "Nginx config does not proxy to upstream port 9090."

def test_nginx_running():
    """Test that Nginx is running as an unprivileged user with the custom config."""
    try:
        result = subprocess.run(["pgrep", "-f", "nginx.*-c /home/user/nginx.conf"], capture_output=True, text=True)
        assert result.returncode == 0 and result.stdout.strip() != "", "Nginx is not running with the custom config."
    except FileNotFoundError:
        # Fallback if pgrep is not available
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        assert "nginx -c /home/user/nginx.conf" in result.stdout or "nginx: master process" in result.stdout, \
            "Nginx is not running with the custom config."

def test_nginx_data_directories():
    """Test that the required Nginx data directories exist."""
    data_dir = "/home/user/nginx_data"
    assert os.path.isdir(data_dir), f"Nginx data directory not found at {data_dir}"