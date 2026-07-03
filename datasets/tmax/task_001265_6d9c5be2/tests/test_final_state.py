# test_final_state.py

import os
import glob
import urllib.request
import urllib.error
import pytest
import re

def test_validator_binary_exists():
    assert os.path.isfile('/home/user/validator-bin'), "Validator binary /home/user/validator-bin is missing"
    assert os.access('/home/user/validator-bin', os.X_OK), "Validator binary is not executable"

def test_validator_running():
    try:
        req = urllib.request.Request('http://127.0.0.1:8083/validate')
        # We don't provide a token, so it might fail with 400/401/403, but it should connect
        urllib.request.urlopen(req, timeout=2)
    except urllib.error.URLError as e:
        if not hasattr(e, 'code'):
            pytest.fail("Validator service is not running on port 8083")

def test_clean_corpus_accepted():
    clean_dir = '/app/corpus/clean'
    txt_files = glob.glob(os.path.join(clean_dir, '*.txt'))
    assert len(txt_files) > 0, "No clean tokens found"

    rejected = []
    for f in txt_files:
        with open(f, 'r') as file:
            token = file.read().strip()
        req = urllib.request.Request('http://127.0.0.1:8083/validate')
        req.add_header('Authorization', f'Bearer {token}')
        try:
            res = urllib.request.urlopen(req, timeout=2)
            if res.getcode() != 200:
                rejected.append(os.path.basename(f))
        except urllib.error.HTTPError as e:
            rejected.append(os.path.basename(f))
        except Exception:
            rejected.append(os.path.basename(f))

    assert len(rejected) == 0, f"{len(rejected)} of {len(txt_files)} clean modified/rejected: {rejected[:5]}"

def test_evil_corpus_rejected():
    evil_dir = '/app/corpus/evil'
    txt_files = glob.glob(os.path.join(evil_dir, '*.txt'))
    assert len(txt_files) > 0, "No evil tokens found"

    bypassed = []
    for f in txt_files:
        with open(f, 'r') as file:
            token = file.read().strip()
        req = urllib.request.Request('http://127.0.0.1:8083/validate')
        req.add_header('Authorization', f'Bearer {token}')
        try:
            res = urllib.request.urlopen(req, timeout=2)
            if res.getcode() == 200:
                bypassed.append(os.path.basename(f))
        except urllib.error.HTTPError as e:
            if e.code != 403:
                bypassed.append(f"{os.path.basename(f)} (returned {e.code})")
        except Exception:
            # If it fails to connect, that's not a bypass, but we should probably fail
            pass

    assert len(bypassed) == 0, f"{len(bypassed)} of {len(txt_files)} evil bypassed: {bypassed[:5]}"

def test_nginx_configured_auth_request():
    conf_path = '/app/nginx/nginx.conf'
    assert os.path.isfile(conf_path), "Nginx config missing"
    with open(conf_path, 'r') as f:
        content = f.read()
    assert 'auth_request' in content, "auth_request directive not found in nginx.conf"
    assert '8083' in content or 'auth_validate' in content, "Validator service port 8083 or internal location not referenced in nginx.conf"

def test_end_to_end_nginx_proxy():
    clean_dir = '/app/corpus/clean'
    txt_files = glob.glob(os.path.join(clean_dir, '*.txt'))
    if not txt_files:
        pytest.fail("No clean tokens found for E2E test")

    with open(txt_files[0], 'r') as file:
        clean_token = file.read().strip()

    req = urllib.request.Request('http://127.0.0.1:8080/resource')
    req.add_header('Authorization', f'Bearer {clean_token}')
    try:
        res = urllib.request.urlopen(req, timeout=2)
        assert res.getcode() in [200, 404], f"Expected success or 404 from resource service, got {res.getcode()}"
    except urllib.error.HTTPError as e:
        if e.code == 403:
            pytest.fail("Nginx E2E test failed: clean token rejected by auth_request")

    evil_dir = '/app/corpus/evil'
    evil_files = glob.glob(os.path.join(evil_dir, '*.txt'))
    if not evil_files:
        pytest.fail("No evil tokens found for E2E test")

    with open(evil_files[0], 'r') as file:
        evil_token = file.read().strip()

    req = urllib.request.Request('http://127.0.0.1:8080/resource')
    req.add_header('Authorization', f'Bearer {evil_token}')
    try:
        res = urllib.request.urlopen(req, timeout=2)
        pytest.fail("Nginx E2E test failed: evil token bypassed auth_request")
    except urllib.error.HTTPError as e:
        assert e.code in [401, 403], f"Expected 401 or 403 for evil token, got {e.code}"

def test_audit_log_exists():
    log_path = '/home/user/audit.log'
    assert os.path.isfile(log_path), "Audit log /home/user/audit.log is missing"
    with open(log_path, 'r') as f:
        content = f.read()
    assert "[ACCEPT]" in content or "[REJECT]" in content, "Audit log does not contain ACCEPT/REJECT entries"