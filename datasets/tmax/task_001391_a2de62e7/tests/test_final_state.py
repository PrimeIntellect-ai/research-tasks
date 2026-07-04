# test_final_state.py
import os
import subprocess
import urllib.request
import ssl
import grp
import stat
import pytest

def test_prober_cli_works():
    prober_path = "/home/user/prober-cli"
    assert os.path.isfile(prober_path), f"{prober_path} does not exist"
    assert os.access(prober_path, os.X_OK), f"{prober_path} is not executable"

    try:
        result = subprocess.run([prober_path, "https://google.com"], capture_output=True, text=True, timeout=10)
    except subprocess.TimeoutExpired:
        pytest.fail("Prober timed out, likely the timeout bug is not fixed.")

    assert result.returncode == 0, f"Prober failed with return code {result.returncode}, output: {result.stderr}"
    assert "STATUS: 200" in result.stdout, f"Expected STATUS: 200 OK in output, got: {result.stdout}"

def test_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), f"{sanitizer_path} does not exist"
    assert os.access(sanitizer_path, os.X_OK), f"{sanitizer_path} is not executable"

    # Evil corpus
    evil_path = "/app/url_corpus/evil/ssrf_urls.txt"
    with open(evil_path, "r") as f:
        evil_urls = [line.strip() for line in f if line.strip()]

    bypassed_evil = []
    for url in evil_urls:
        result = subprocess.run([sanitizer_path], input=url + "\n", capture_output=True, text=True)
        out = result.stdout.strip()
        if out:
            bypassed_evil.append(url)

    # Clean corpus
    clean_path = "/app/url_corpus/clean/valid_urls.txt"
    with open(clean_path, "r") as f:
        clean_urls = [line.strip() for line in f if line.strip()]

    modified_clean = []
    for url in clean_urls:
        result = subprocess.run([sanitizer_path], input=url + "\n", capture_output=True, text=True)
        out = result.stdout.strip()
        if out != url:
            modified_clean.append(url)

    error_msgs = []
    if bypassed_evil:
        error_msgs.append(f"{len(bypassed_evil)} of {len(evil_urls)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msgs.append(f"{len(modified_clean)} of {len(clean_urls)} clean modified: {', '.join(modified_clean)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))

def test_tls_certificates_and_server():
    assert os.path.isfile("/home/user/server.crt"), "server.crt is missing"
    assert os.path.isfile("/home/user/server.key"), "server.key is missing"

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://127.0.0.1:8443/health")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
    except Exception as e:
        pytest.fail(f"Failed to connect to HTTPS server on 127.0.0.1:8443/health: {e}")

def test_log_file_permissions_and_group():
    log_path = "/var/log/prober.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist"

    st = os.stat(log_path)

    # Check permissions 640
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o640, f"Expected permissions 640 (0o640), got {oct(perms)}"

    # Check group sre-logs
    try:
        group_info = grp.getgrgid(st.st_gid)
        group_name = group_info.gr_name
    except KeyError:
        group_name = str(st.st_gid)

    assert group_name == "sre-logs", f"Expected group sre-logs, got {group_name}"