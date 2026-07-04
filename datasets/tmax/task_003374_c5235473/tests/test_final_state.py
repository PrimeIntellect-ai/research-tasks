# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_nginx_config_fixed():
    conf_path = "/app/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"Nginx config not found at {conf_path}"
    with open(conf_path, "r") as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:8081;" in content, "Nginx config not correctly updated to proxy to 127.0.0.1:8081."

def test_backend_env_fixed():
    env_path = "/app/backend/.env"
    assert os.path.isfile(env_path), f"Backend .env not found at {env_path}"
    with open(env_path, "r") as f:
        content = f.read()
    assert "REDIS_URL=redis://127.0.0.1:6379" in content, "Backend .env not correctly updated to point to local Redis."

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def test_end_to_end_flow():
    opener = urllib.request.build_opener(NoRedirectHandler())
    try:
        response = opener.open("http://127.0.0.1:8080/api/login?redirect=http://example.com", timeout=5)
        status = response.status
        location = response.getheader("Location")
    except urllib.error.HTTPError as e:
        status = e.code
        location = e.headers.get("Location")
    except Exception as e:
        pytest.fail(f"Failed to perform end-to-end request. Are the services running? Error: {e}")

    assert status == 302, f"Expected HTTP 302 Found, got {status}"
    assert location == "http://example.com", f"Expected Location header 'http://example.com', got '{location}'"

def test_waf_filter_binary_exists():
    binary_path = "/home/user/waf_filter/target/release/waf_filter"
    assert os.path.isfile(binary_path), f"WAF filter binary not found at {binary_path}. Did you compile with --release?"
    assert os.access(binary_path, os.X_OK), f"WAF filter binary at {binary_path} is not executable"

def test_waf_filter_corpus():
    binary_path = "/home/user/waf_filter/target/release/waf_filter"
    if not os.path.isfile(binary_path):
        pytest.skip("WAF filter binary not found, skipping corpus test.")

    evil_dir = "/app/corpus/evil"
    clean_dir = "/app/corpus/clean"

    evil_failed = []
    clean_failed = []

    evil_total = 0
    clean_total = 0

    # Test Evil Corpus
    for root, _, files in os.walk(evil_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                urls = f.read().splitlines()

            for url in urls:
                if not url.strip():
                    continue
                evil_total += 1
                proc = subprocess.run([binary_path], input=url.strip(), text=True, capture_output=True)
                output = proc.stdout.strip()
                if output != "EVIL":
                    evil_failed.append((file, url, output))

    # Test Clean Corpus
    for root, _, files in os.walk(clean_dir):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, "r") as f:
                urls = f.read().splitlines()

            for url in urls:
                if not url.strip():
                    continue
                clean_total += 1
                proc = subprocess.run([binary_path], input=url.strip(), text=True, capture_output=True)
                output = proc.stdout.strip()
                if output != "CLEAN":
                    clean_failed.append((file, url, output))

    error_msg = []
    if evil_failed:
        offending_files = ", ".join(set(f[0] for f in evil_failed))
        error_msg.append(f"{len(evil_failed)} of {evil_total} evil bypassed. Offending files: {offending_files}")
    if clean_failed:
        offending_files = ", ".join(set(f[0] for f in clean_failed))
        error_msg.append(f"{len(clean_failed)} of {clean_total} clean modified/rejected. Offending files: {offending_files}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))