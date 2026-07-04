# test_final_state.py
import os
import urllib.request
import urllib.error

def test_nginx_config_fixed():
    nginx_conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.exists(nginx_conf_path), f"Nginx config not found at {nginx_conf_path}"
    with open(nginx_conf_path, "r") as f:
        content = f.read()
        assert "proxy_pass http://127.0.0.1:8080;" in content, "Nginx config was not updated to point to port 8080."

def test_symlink_and_directories():
    app_logs_dir = "/home/user/app_logs"
    app_logs_symlink = "/home/user/app/logs"

    assert os.path.isdir(app_logs_dir), f"Directory {app_logs_dir} does not exist."
    assert os.path.islink(app_logs_symlink), f"{app_logs_symlink} is not a symlink."

    target = os.readlink(app_logs_symlink)
    assert target == app_logs_dir, f"Symlink {app_logs_symlink} points to {target}, expected {app_logs_dir}."

def test_post_receive_hook():
    hook_path = "/home/user/repo.git/hooks/post-receive"
    assert os.path.exists(hook_path), f"Git hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Git hook at {hook_path} is not executable."

def test_startup_log_utc():
    log_path = "/home/user/app_logs/startup.log"
    assert os.path.exists(log_path), f"Startup log not found at {log_path}. Did the backend run successfully?"

    with open(log_path, "r") as f:
        content = f.read()
        assert "UTC" in content, "The startup log does not contain a UTC timestamp. Ensure TZ=UTC is set."

def test_nginx_response():
    url = "http://127.0.0.1:8000"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")

            assert status == 200, f"Expected HTTP 200, got {status}"
            assert "Backend running!" in body, f"Expected 'Backend running!' in response, got: {body}"
    except urllib.error.URLError as e:
        assert False, f"Failed to connect to Nginx on port 8000: {e}"