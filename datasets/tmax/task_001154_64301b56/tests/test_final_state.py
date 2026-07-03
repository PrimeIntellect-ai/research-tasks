# test_final_state.py

import os
import re
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_malicious_ips_file():
    filepath = "/home/user/malicious_ips.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_ips = ["198.51.100.7", "203.0.113.42"]
    assert lines == expected_ips, f"Expected IPs {expected_ips}, but got {lines} in {filepath}"

def test_block_rules_file():
    filepath = "/home/user/block_rules.sh"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "iptables -A INPUT -s 198.51.100.7 -j DROP",
        "iptables -A INPUT -s 203.0.113.42 -j DROP"
    ]

    # Filter out shebang if present
    actual_rules = [line for line in lines if not line.startswith('#')]
    assert actual_rules == expected_lines, f"Expected block rules {expected_lines}, but got {actual_rules} in {filepath}"

@pytest.fixture(scope="module")
def running_app():
    app_path = "/home/user/app.py"
    assert os.path.isfile(app_path), f"File {app_path} is missing."

    process = subprocess.Popen(["python3", app_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # Give Flask time to start

    yield process

    process.terminate()
    process.wait()

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def test_app_csp_header(running_app):
    opener = urllib.request.build_opener(NoRedirectHandler())
    try:
        response = opener.open('http://127.0.0.1:5000/dashboard', timeout=5)
        csp = response.getheader('Content-Security-Policy')
        assert csp == "default-src 'self'", f"Expected CSP header \"default-src 'self'\", got {csp}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to app: {e}")

def test_app_valid_relative_redirect(running_app):
    opener = urllib.request.build_opener(NoRedirectHandler())
    try:
        response = opener.open('http://127.0.0.1:5000/login?next=/settings', timeout=5)
        assert response.status == 302, f"Expected 302 redirect, got {response.status}"
        loc = response.getheader('Location')
        assert loc in ['/settings', 'http://127.0.0.1:5000/settings'], f"Valid relative redirect failed, got Location: {loc}"
    except urllib.error.HTTPError as e:
        if e.code == 302:
            loc = e.headers.get('Location')
            assert loc in ['/settings', 'http://127.0.0.1:5000/settings'], f"Valid relative redirect failed, got Location: {loc}"
        else:
            pytest.fail(f"HTTP Error: {e}")

def test_app_absolute_url_redirect_blocked(running_app):
    opener = urllib.request.build_opener(NoRedirectHandler())
    try:
        response = opener.open('http://127.0.0.1:5000/login?next=http://evil.com', timeout=5)
        pytest.fail("Expected redirect, but got 200 OK")
    except urllib.error.HTTPError as e:
        if e.code == 302:
            loc = e.headers.get('Location')
            assert loc in ['/dashboard', 'http://127.0.0.1:5000/dashboard'], f"Absolute URL redirect not blocked, got Location: {loc}"
        else:
            pytest.fail(f"HTTP Error: {e}")

def test_app_protocol_relative_redirect_blocked(running_app):
    opener = urllib.request.build_opener(NoRedirectHandler())
    try:
        response = opener.open('http://127.0.0.1:5000/login?next=//evil.com', timeout=5)
        pytest.fail("Expected redirect, but got 200 OK")
    except urllib.error.HTTPError as e:
        if e.code == 302:
            loc = e.headers.get('Location')
            assert loc in ['/dashboard', 'http://127.0.0.1:5000/dashboard'], f"Protocol-relative redirect not blocked, got Location: {loc}"
        else:
            pytest.fail(f"HTTP Error: {e}")