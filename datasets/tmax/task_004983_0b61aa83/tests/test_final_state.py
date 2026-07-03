# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_nginx_config_updated():
    config_path = "/home/user/nginx.conf"
    assert os.path.exists(config_path), f"Nginx config missing at {config_path}"
    with open(config_path, 'r') as f:
        content = f.read()

    assert "proxy_pass" in content and "8081" in content, "Nginx config does not contain proxy_pass to port 8081"

def test_adversarial_corpus():
    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_modified = []

    url = "http://127.0.0.1:8080/api/query"

    # Test Evil Corpus (Must return 403 Forbidden)
    for f in evil_files:
        filepath = os.path.join(evil_dir, f)
        with open(filepath, 'rb') as fd:
            data = fd.read()

        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                # If it succeeds (200 OK) or returns something else, it bypassed the filter
                if response.status != 403:
                    evil_bypassed.append(f)
        except urllib.error.HTTPError as e:
            if e.code != 403:
                evil_bypassed.append(f)
        except Exception:
            # Connection errors or timeouts are considered failures to properly handle the request
            evil_bypassed.append(f)

    # Test Clean Corpus (Must return 200 OK)
    for f in clean_files:
        filepath = os.path.join(clean_dir, f)
        with open(filepath, 'rb') as fd:
            data = fd.read()

        req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=3) as response:
                if response.status != 200:
                    clean_modified.append(f)
        except urllib.error.HTTPError as e:
            clean_modified.append(f)
        except Exception:
            clean_modified.append(f)

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not evil_bypassed and not clean_modified, " ; ".join(error_msgs)