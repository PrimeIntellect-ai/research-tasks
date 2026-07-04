# test_final_state.py

import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_sanitizer_adversarial_corpus():
    sanitizer_bin = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_bin), f"Sanitizer binary not found at {sanitizer_bin}"
    assert os.access(sanitizer_bin, os.X_OK), f"Sanitizer binary is not executable"

    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing: {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing: {clean_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    assert len(evil_files) > 0, "No evil files found in corpus."
    assert len(clean_files) > 0, "No clean files found in corpus."

    evil_bypassed = []
    for f in evil_files:
        result = subprocess.run([sanitizer_bin, f], capture_output=True)
        if result.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        result = subprocess.run([sanitizer_bin, f], capture_output=True)
        if result.returncode != 0:
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not errors, " | ".join(errors)

def test_nginx_routing_config():
    nginx_conf = "/app/nginx/nginx.conf"
    assert os.path.isfile(nginx_conf), f"Nginx configuration not found at {nginx_conf}"

    with open(nginx_conf, "r") as f:
        conf = f.read()

    assert "proxy_pass" in conf, "Nginx config missing proxy_pass directives."
    assert "9001" in conf, "Nginx config missing routing to port 9001 (Storage Backend)."
    assert "9002" in conf, "Nginx config missing routing to port 9002 (Execution Backend)."

def test_nginx_services_running_and_routing():
    # Test /api/patch routing
    try:
        req_patch = urllib.request.urlopen("http://localhost:8080/api/patch", timeout=5)
        patch_code = req_patch.getcode()
    except urllib.error.HTTPError as e:
        patch_code = e.code
    except Exception as e:
        pytest.fail(f"Failed to connect to /api/patch via Nginx. Are the services running? Error: {e}")

    # Test /api/asm routing
    try:
        req_asm = urllib.request.urlopen("http://localhost:8080/api/asm", timeout=5)
        asm_code = req_asm.getcode()
    except urllib.error.HTTPError as e:
        asm_code = e.code
    except Exception as e:
        pytest.fail(f"Failed to connect to /api/asm via Nginx. Are the services running? Error: {e}")

    # If Nginx is running but proxy_pass is wrong or backend is down, it typically returns 502.
    # If no route is defined, it typically returns 404 from Nginx itself.
    assert patch_code != 502, "/api/patch returned 502 Bad Gateway, meaning proxy_pass failed to reach port 9001."
    assert asm_code != 502, "/api/asm returned 502 Bad Gateway, meaning proxy_pass failed to reach port 9002."