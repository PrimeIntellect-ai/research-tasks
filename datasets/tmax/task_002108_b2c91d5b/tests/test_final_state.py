# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_nginx_proxy_fixed():
    """Verify that Nginx successfully proxies to the backend returning HTTP 200."""
    try:
        req = urllib.request.Request("http://127.0.0.1:8080/")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected 200 OK, got {response.status}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Nginx returned HTTP Error: {e.code} (Backend still not correctly proxied or Nginx not reloaded)")
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Nginx on port 8080: {e.reason}")

def test_logrotate_config():
    """Verify the logrotate config contains the required directives."""
    config_path = "/home/user/logrotate.conf"
    assert os.path.exists(config_path), f"logrotate configuration file not found at {config_path}"

    with open(config_path, "r") as f:
        content = f.read().lower()

    # Check for target path
    assert "/home/user/nginx/logs/" in content and ".log" in content, "Target log path (/home/user/nginx/logs/*.log) not found in logrotate config"

    # Check for required directives
    assert "daily" in content, "'daily' directive missing from logrotate config"
    assert "rotate 7" in content, "'rotate 7' directive missing from logrotate config"
    assert "compress" in content, "'compress' directive missing from logrotate config"
    assert "missingok" in content, "'missingok' directive missing from logrotate config"

    # Validate syntax using logrotate debug mode
    res = subprocess.run(["logrotate", "-d", config_path], capture_output=True, text=True)
    assert res.returncode == 0, f"logrotate configuration syntax is invalid: {res.stderr}"

def test_waf_script_adversarial_corpus():
    """Verify the WAF script correctly handles the evil and clean corpora."""
    waf_path = "/home/user/waf.sh"
    assert os.path.exists(waf_path), f"WAF script not found at {waf_path}"

    evil_path = "/home/user/corpora/evil.txt"
    clean_path = "/home/user/corpora/clean.txt"

    assert os.path.exists(evil_path), "Evil corpus missing"
    assert os.path.exists(clean_path), "Clean corpus missing"

    with open(evil_path, "r") as f:
        evil_lines = [line.strip() for line in f if line.strip()]

    with open(clean_path, "r") as f:
        clean_lines = [line.strip() for line in f if line.strip()]

    evil_bypassed = []
    for line in evil_lines:
        res = subprocess.run(["bash", waf_path, line], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(line)

    clean_modified = []
    for line in clean_lines:
        res = subprocess.run(["bash", waf_path, line], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(line)

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_lines)} evil bypassed. Offending examples: {evil_bypassed[:3]}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_lines)} clean modified (rejected). Offending examples: {clean_modified[:3]}")

    assert not evil_bypassed and not clean_modified, " | ".join(errors)