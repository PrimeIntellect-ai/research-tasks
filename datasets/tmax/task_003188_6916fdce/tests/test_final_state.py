# test_final_state.py
import os
import re
import urllib.request
import urllib.error
import pytest

def test_config_symlink_fixed():
    symlink_path = '/home/user/service/config.json'
    assert os.path.exists(symlink_path), f"Symlink {symlink_path} does not exist."
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."
    target = os.readlink(symlink_path)
    expected_target = '/home/user/service/configs/production.json'
    assert target == expected_target, f"Symlink points to {target} instead of {expected_target}."

def test_cache_directory_created():
    cache_dir = '/home/user/service/cache'
    assert os.path.exists(cache_dir), f"Cache directory {cache_dir} does not exist."
    assert os.path.isdir(cache_dir), f"{cache_dir} is not a directory."

def test_supervisor_script_exists_and_valid():
    script_path = '/home/user/service/supervisor.sh'
    assert os.path.exists(script_path), f"Supervisor script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    with open(script_path, 'r') as f:
        content = f.read()

    # Check for a while loop
    assert re.search(r'\bwhile\b', content), "Supervisor script does not contain a 'while' loop."
    # Check for daemon execution
    assert 'daemon.py' in content, "Supervisor script does not seem to execute daemon.py."

def test_health_check_output():
    health_file = '/home/user/service/health_check.txt'
    assert os.path.exists(health_file), f"Health check output file {health_file} does not exist."
    assert os.path.isfile(health_file), f"{health_file} is not a file."

    with open(health_file, 'r') as f:
        content = f.read().strip()

    expected_output = '{"status": "healthy", "uptime": "stable"}'
    assert content == expected_output, f"Health check file content is incorrect. Expected: '{expected_output}', Got: '{content}'"

def test_service_is_running():
    # Verify that the service is actually listening and responding
    url = 'http://127.0.0.1:8181/health'
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            assert response.status == 200, f"Service returned HTTP {response.status} instead of 200."
            data = response.read().decode('utf-8').strip()
            assert data == '{"status": "healthy", "uptime": "stable"}', "Service returned unexpected payload."
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to the service at {url}. Is the supervisor running in the background? Error: {e}")