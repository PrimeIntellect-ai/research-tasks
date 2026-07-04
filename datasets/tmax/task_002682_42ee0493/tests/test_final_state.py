# test_final_state.py

import os
import urllib.request
import urllib.error
import stat
import time

def test_deploy_script_exists_and_executable():
    """Check if the deploy script exists and is executable."""
    deploy_script_path = "/home/user/deploy.sh"
    assert os.path.exists(deploy_script_path), f"Deploy script not found at {deploy_script_path}"
    assert os.path.isfile(deploy_script_path), f"{deploy_script_path} is not a file"

    st = os.stat(deploy_script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Deploy script {deploy_script_path} is not executable"

def test_app_current_is_symlink():
    """Check if /home/user/app/current is a symbolic link."""
    current_path = "/home/user/app/current"
    assert os.path.exists(current_path), f"Symlink target {current_path} does not exist"
    assert os.path.islink(current_path), f"{current_path} is not a symbolic link"

def test_backend_service_exists():
    """Check if the backend_service executable exists in the current release."""
    backend_service_path = "/home/user/app/current/backend_service"
    assert os.path.exists(backend_service_path), f"Backend service executable not found at {backend_service_path}"
    assert os.path.isfile(backend_service_path), f"{backend_service_path} is not a file"

    st = os.stat(backend_service_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Backend service {backend_service_path} is not executable"

def test_nginx_and_backend_integration():
    """Check if Nginx is serving the backend service correctly."""
    url = "http://localhost:8080/"

    # Try a few times to allow services to start if they were just restarted
    max_retries = 3
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                body = response.read().decode('utf-8').strip()

                assert status == 200, f"Expected HTTP 200, got {status}"
                assert body == "SUCCESS_DEPLOYMENT", f"Expected response body 'SUCCESS_DEPLOYMENT', got '{body}'"
                return # Success
        except urllib.error.URLError as e:
            if attempt == max_retries - 1:
                assert False, f"Failed to connect to Nginx on port 8080: {e}"
            time.sleep(1)