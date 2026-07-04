# test_final_state.py

import os
import pwd
import grp
import stat
import subprocess
import requests
import pytest

def test_setup_script_idempotence():
    """Run /home/user/setup.sh twice to verify idempotence."""
    setup_script = '/home/user/setup.sh'
    assert os.path.isfile(setup_script), f"{setup_script} does not exist."
    assert os.access(setup_script, os.X_OK), f"{setup_script} is not executable."

    # Run first time
    result1 = subprocess.run([setup_script], capture_output=True, text=True)
    assert result1.returncode == 0, f"First run of setup.sh failed: {result1.stderr}"

    # Run second time
    result2 = subprocess.run([setup_script], capture_output=True, text=True)
    assert result2.returncode == 0, f"Second run of setup.sh failed (not idempotent): {result2.stderr}"

def test_user_and_group_setup():
    """Check if group webfiles and user tinyweb_usr exist with correct settings."""
    try:
        group = grp.getgrnam('webfiles')
    except KeyError:
        pytest.fail("Group 'webfiles' does not exist.")

    try:
        user = pwd.getpwnam('tinyweb_usr')
    except KeyError:
        pytest.fail("User 'tinyweb_usr' does not exist.")

    assert user.pw_shell == '/usr/sbin/nologin', f"tinyweb_usr shell is {user.pw_shell}, expected /usr/sbin/nologin"
    assert user.pw_gid == group.gr_gid or group.gr_name in [g.gr_name for g in grp.getgrall() if user.pw_name in g.gr_mem], "tinyweb_usr is not in webfiles group."

def test_filesystem_and_permissions():
    """Check /var/www/html permissions and index.html content."""
    web_dir = '/var/www/html'
    index_file = os.path.join(web_dir, 'index.html')

    assert os.path.isdir(web_dir), f"{web_dir} does not exist."

    dir_stat = os.stat(web_dir)
    assert pwd.getpwuid(dir_stat.st_uid).pw_name == 'root', f"{web_dir} is not owned by root."
    assert grp.getgrgid(dir_stat.st_gid).gr_name == 'webfiles', f"{web_dir} group is not webfiles."

    # Check permissions: group read, others no access
    assert bool(dir_stat.st_mode & stat.S_IRGRP), f"{web_dir} is not readable by group."
    assert not bool(dir_stat.st_mode & stat.S_IROTH), f"{web_dir} is readable by others."

    assert os.path.isfile(index_file), f"{index_file} does not exist."
    with open(index_file, 'r') as f:
        content = f.read().strip()
    assert "Welcome to the secure server" in content, f"Unexpected content in {index_file}: {content}"

def test_tls_certificates_exist():
    """Check if TLS certificates exist."""
    cert_path = '/etc/tinyweb/cert.pem'
    key_path = '/etc/tinyweb/key.pem'

    assert os.path.isfile(cert_path), f"{cert_path} does not exist."
    assert os.path.isfile(key_path), f"{key_path} does not exist."

def test_web_server_running_and_serving():
    """Test if the web server is running on 8443 and serves index.html over HTTPS."""
    url = "https://127.0.0.1:8443/index.html"
    try:
        response = requests.get(url, verify=False, timeout=5)
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "Welcome to the secure server" in response.text, "Response body does not contain the expected message."
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")