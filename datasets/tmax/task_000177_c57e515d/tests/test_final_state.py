# test_final_state.py

import os
import json
import urllib.request
import urllib.error
import subprocess
import glob
import pytest

def test_nginx_config_auth_request():
    nginx_conf_path = "/app/testbed/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"Nginx configuration file missing at {nginx_conf_path}"

    with open(nginx_conf_path, 'r') as f:
        content = f.read()

    assert "auth_request" in content, "Nginx configuration does not use auth_request directive"
    assert "9000" in content, "Nginx configuration does not reference the WAF port 9000"

def test_iptables_rules():
    result = subprocess.run(["iptables-save"], capture_output=True, text=True)
    output = result.stdout

    # Check if there are DROP rules for 5000 and 6379
    assert "5000" in output and "6379" in output, "iptables rules for ports 5000 and 6379 are missing"
    assert "-j DROP" in output, "iptables rules do not contain a DROP policy for the exposed ports"
    assert "-i lo" in output and "-j ACCEPT" in output, "iptables rules do not contain an ACCEPT policy for the loopback interface"

def test_adversarial_corpus():
    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))

    assert len(evil_files) > 0, "No evil corpus files found"
    assert len(clean_files) > 0, "No clean corpus files found"

    evil_bypassed = []
    clean_modified = []

    url = "http://127.0.0.1:8080/"

    for filepath in evil_files:
        with open(filepath, 'rb') as f:
            data = f.read()

        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            response = urllib.request.urlopen(req, timeout=5)
            # If we get here, it means it returned 200 OK, which is a bypass
            evil_bypassed.append(os.path.basename(filepath))
        except urllib.error.HTTPError as e:
            if e.code != 403:
                evil_bypassed.append(f"{os.path.basename(filepath)} (HTTP {e.code})")
        except Exception as e:
            evil_bypassed.append(f"{os.path.basename(filepath)} (Error: {e})")

    for filepath in clean_files:
        with open(filepath, 'rb') as f:
            data = f.read()

        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            response = urllib.request.urlopen(req, timeout=5)
            if response.getcode() != 200:
                clean_modified.append(f"{os.path.basename(filepath)} (HTTP {response.getcode()})")
        except urllib.error.HTTPError as e:
            clean_modified.append(f"{os.path.basename(filepath)} (HTTP {e.code})")
        except Exception as e:
            clean_modified.append(f"{os.path.basename(filepath)} (Error: {e})")

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/blocked: {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, " | ".join(error_msgs)