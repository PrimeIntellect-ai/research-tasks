# test_final_state.py

import os
import stat
import subprocess
import tempfile
import requests
import pytest

def test_permissions_fixed():
    bin_dir = "/app/vulnerable_stack/bin"
    assert os.path.isdir(bin_dir), f"Directory {bin_dir} is missing."

    for filename in os.listdir(bin_dir):
        filepath = os.path.join(bin_dir, filename)
        if os.path.isfile(filepath):
            st = os.stat(filepath)
            mode = st.st_mode
            assert not (mode & stat.S_ISUID), f"File {filepath} still has the SUID bit set."
            assert not (mode & stat.S_IWOTH), f"File {filepath} is still world-writable."
            assert (mode & stat.S_IXUSR), f"File {filepath} should be executable by the owner."

def test_detect_script():
    script_path = "/home/user/detect.sh"
    assert os.path.isfile(script_path), f"Intrusion detection script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    dummy_log = """192.168.1.10 - - [10/Oct/2023:13:55:36 -0700] "GET /login?next=http://evil.com HTTP/1.1" 302 5 "-" "curl"
192.168.1.11 - - [10/Oct/2023:13:55:37 -0700] "GET /login?next=https://bad.com HTTP/1.1" 302 5 "-" "curl"
192.168.1.10 - - [10/Oct/2023:13:55:38 -0700] "GET /login?next=//attacker.com HTTP/1.1" 302 5 "-" "curl"
10.0.0.1 - - [10/Oct/2023:13:55:39 -0700] "GET /login?next=/dashboard HTTP/1.1" 302 5 "-" "curl"
192.168.1.12 - - [10/Oct/2023:13:55:40 -0700] "GET /login?next=http://malware.com HTTP/1.1" 302 5 "-" "curl"
10.0.0.2 - - [10/Oct/2023:13:55:41 -0700] "GET /index.html HTTP/1.1" 200 100 "-" "curl"
"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmp:
        tmp.write(dummy_log)
        tmp_path = tmp.name

    try:
        result = subprocess.run(['bash', script_path, tmp_path], capture_output=True, text=True, timeout=5)
        assert result.returncode == 0, f"Script failed with exit code {result.returncode}. Stderr: {result.stderr}"

        output_ips = set(line.strip() for line in result.stdout.strip().split('\n') if line.strip())
        expected_ips = {"192.168.1.10", "192.168.1.11", "192.168.1.12"}

        assert output_ips == expected_ips, f"Expected IPs {expected_ips}, but got {output_ips}"
    finally:
        os.remove(tmp_path)

def test_open_redirect_patched():
    base_url = "http://127.0.0.1:8080/login"

    # Test valid internal redirect
    try:
        resp1 = requests.get(f"{base_url}?next=/internal", allow_redirects=False, timeout=5)
        assert resp1.status_code == 302, f"Expected HTTP 302 for valid internal redirect, got {resp1.status_code}"
        assert resp1.headers.get('Location') == '/internal', f"Expected Location: /internal, got {resp1.headers.get('Location')}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to Nginx on port 8080: {e}")

    # Test malicious external redirect (http)
    resp2 = requests.get(f"{base_url}?next=http://malicious.com", allow_redirects=False, timeout=5)
    assert resp2.status_code == 302, f"Expected HTTP 302 for malicious redirect, got {resp2.status_code}"
    assert resp2.headers.get('Location') == '/', f"Expected Location: / for malicious redirect, got {resp2.headers.get('Location')}"

    # Test malicious external redirect (protocol relative)
    resp3 = requests.get(f"{base_url}?next=//attacker.com", allow_redirects=False, timeout=5)
    assert resp3.status_code == 302, f"Expected HTTP 302 for malicious redirect, got {resp3.status_code}"
    assert resp3.headers.get('Location') == '/', f"Expected Location: / for malicious redirect, got {resp3.headers.get('Location')}"