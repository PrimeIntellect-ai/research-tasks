# test_final_state.py
import os
import re
import subprocess
import pytest

def test_success_log_content():
    log_path = "/home/user/success.log"
    assert os.path.isfile(log_path), f"Expected file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "Hello from the backend!" in content, (
        f"File {log_path} does not contain the expected success message. "
        f"Found: {content.strip()}"
    )

def test_backend_cache_directory_exists():
    cache_dir = "/home/user/backend/cache"
    assert os.path.isdir(cache_dir), f"The backend cache directory {cache_dir} was not created."

def test_bash_profile_contains_backend_port():
    profile_path = "/home/user/.bash_profile"
    assert os.path.isfile(profile_path), f"File {profile_path} is missing."

    with open(profile_path, "r") as f:
        content = f.read()

    # Look for export BACKEND_PORT=<port>
    match = re.search(r'export\s+BACKEND_PORT=(\d+)', content)
    assert match is not None, "BACKEND_PORT environment variable is not exported in .bash_profile."

    port = int(match.group(1))
    assert port > 1024, f"BACKEND_PORT {port} should be a high, unused port."

def test_nginx_config_updated_with_correct_port():
    profile_path = "/home/user/.bash_profile"
    with open(profile_path, "r") as f:
        content = f.read()
    match = re.search(r'export\s+BACKEND_PORT=(\d+)', content)
    if not match:
        pytest.fail("Cannot verify nginx config because BACKEND_PORT is not in .bash_profile")

    backend_port = match.group(1)

    config_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(config_path), f"Nginx config {config_path} is missing."

    with open(config_path, "r") as f:
        config_content = f.read()

    expected_proxy_pass = f"proxy_pass http://127.0.0.1:{backend_port};"
    assert expected_proxy_pass in config_content or f"proxy_pass http://localhost:{backend_port};" in config_content, (
        f"Nginx config does not contain the correct proxy_pass directive for port {backend_port}."
    )

def test_backend_process_running():
    profile_path = "/home/user/.bash_profile"
    with open(profile_path, "r") as f:
        content = f.read()
    match = re.search(r'export\s+BACKEND_PORT=(\d+)', content)
    if not match:
        pytest.fail("Cannot verify backend process because BACKEND_PORT is not in .bash_profile")

    backend_port = match.group(1)

    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
        assert backend_port in output and "python3" in output, (
            f"Backend process (python3 -m http.server {backend_port}) does not appear to be running."
        )
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run ps aux to check for backend process.")