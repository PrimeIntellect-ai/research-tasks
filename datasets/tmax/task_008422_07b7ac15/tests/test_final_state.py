# test_final_state.py

import os
import ssl
import urllib.request
import subprocess
import pytest

def test_user_prov_executable():
    executable_path = "/home/user/user_prov"
    assert os.path.isfile(executable_path), f"Executable missing: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File is not executable: {executable_path}"

def test_profiles_generated():
    expected_profiles = {
        "alice": "engineering",
        "bob": "sales",
        "charlie": "hr"
    }

    for user, dept in expected_profiles.items():
        profile_path = f"/home/user/public_html/{user}_profile.txt"
        assert os.path.isfile(profile_path), f"Profile missing: {profile_path}"

        with open(profile_path, "r") as f:
            content = f.read()

        assert f"USER:{user}" in content, f"Profile for {user} missing USER field"
        assert f"DEPT:{dept}" in content, f"Profile for {user} missing DEPT field"
        assert "STATUS:ACTIVE" in content, f"Profile for {user} missing STATUS field"

def test_log_file_exists():
    log_path = "/home/user/logs/webserver.log"
    assert os.path.isfile(log_path), f"Log file missing: {log_path}"

def test_supervisor_running():
    try:
        output = subprocess.check_output(["pgrep", "-f", "supervisord.*supervisord.conf"]).decode()
        assert output.strip() != "", "supervisord with custom conf is not running"
    except subprocess.CalledProcessError:
        pytest.fail("supervisord process using /home/user/supervisord.conf not found")

def test_https_server():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:8443/alice_profile.txt"
    try:
        with urllib.request.urlopen(url, context=ctx, timeout=5) as response:
            content = response.read().decode('utf-8')
            assert "USER:alice" in content, "HTTPS response missing expected USER content"
            assert "DEPT:engineering" in content, "HTTPS response missing expected DEPT content"
    except Exception as e:
        pytest.fail(f"Failed to fetch {url} over HTTPS: {e}")