# test_final_state.py

import os
import sys
import pytest
import urllib.request
import urllib.error

# Add the app directory to the path so we can import the sanitizer
sys.path.insert(0, "/home/user/app")

def test_sanitizer_adversarial_corpus():
    try:
        from sanitizer import is_safe_query
    except ImportError:
        pytest.fail("Could not import is_safe_query from /home/user/app/sanitizer.py. Did you create the file and function correctly?")

    evil_dir = "/home/user/tests/corpora/evil/"
    clean_dir = "/home/user/tests/corpora/clean/"

    evil_failed = []
    if os.path.isdir(evil_dir):
        for filename in os.listdir(evil_dir):
            filepath = os.path.join(evil_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                try:
                    if is_safe_query(content) is not False:
                        evil_failed.append(filename)
                except Exception as e:
                    evil_failed.append(f"{filename} (raised {type(e).__name__})")

    clean_failed = []
    if os.path.isdir(clean_dir):
        for filename in os.listdir(clean_dir):
            filepath = os.path.join(clean_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                try:
                    if is_safe_query(content) is not True:
                        clean_failed.append(filename)
                except Exception as e:
                    clean_failed.append(f"{filename} (raised {type(e).__name__})")

    error_msg = []
    if evil_failed:
        error_msg.append(f"{len(evil_failed)} evil files bypassed the sanitizer: {', '.join(evil_failed)}")
    if clean_failed:
        error_msg.append(f"{len(clean_failed)} clean files were incorrectly blocked: {', '.join(clean_failed)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))

def test_nginx_configuration():
    nginx_conf_path = "/home/user/app/nginx.conf"
    assert os.path.isfile(nginx_conf_path), f"{nginx_conf_path} does not exist"

    with open(nginx_conf_path, 'r', encoding='utf-8') as f:
        conf_content = f.read()

    # Check for proxy_pass to port 8000
    assert "proxy_pass" in conf_content, "nginx.conf is missing a proxy_pass directive"
    assert "127.0.0.1:8000" in conf_content or "localhost:8000" in conf_content, "nginx.conf does not proxy to port 8000"

def test_nginx_proxy_live():
    # Attempt to hit the Nginx endpoint to ensure it's up and proxying
    # We expect either a 200, 400, or 405 depending on the GraphQL implementation, 
    # but not a 502 (Bad Gateway) or connection refused.
    req = urllib.request.Request("http://127.0.0.1:8080/graphql", method="POST")
    try:
        urllib.request.urlopen(req, timeout=2)
    except urllib.error.HTTPError as e:
        # HTTP errors from the backend mean the proxy is working
        assert e.code != 502, "Nginx returned 502 Bad Gateway. Is FastAPI running and Nginx configured correctly?"
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to Nginx on port 8080: {e}")