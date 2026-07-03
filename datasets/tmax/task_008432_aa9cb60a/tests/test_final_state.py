# test_final_state.py

import os
import subprocess
import urllib.request
import stat

def test_web_backend_service_fixed():
    service_file = "/home/user/.config/systemd/user/web-backend.service"
    assert os.path.isfile(service_file), f"Missing {service_file}"

    with open(service_file, "r") as f:
        content = f.read()

    assert "After=log-sink.service" in content, "web-backend.service is missing 'After=log-sink.service'"
    assert "Requires=log-sink.service" in content, "web-backend.service is missing 'Requires=log-sink.service'"

def test_services_active():
    services = ["log-sink.service", "web-backend.service", "frontend-proxy.service"]
    for svc in services:
        result = subprocess.run(
            ["systemctl", "--user", "is-active", svc],
            capture_output=True, text=True
        )
        assert result.stdout.strip() == "active", f"Service {svc} is not active. Output: {result.stdout}"

def test_frontend_proxy_working():
    try:
        req = urllib.request.Request("http://127.0.0.1:8443")
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode("utf-8")
            assert "Hello from backend" in body, "Proxy did not return expected response from backend."
    except Exception as e:
        assert False, f"Failed to connect to frontend proxy on port 8443: {e}"

def test_symlink_created():
    symlink_path = "/home/user/app/current_logs"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    # Allow with or without trailing slash
    assert target in ["/home/user/app/logs", "/home/user/app/logs/"], f"Symlink points to wrong target: {target}"

def test_rotate_script():
    script_path = "/home/user/app/rotate.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

    # Ensure server.log exists before rotation
    log_file = "/home/user/app/logs/server.log"
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            f.write("Dummy log line\n")

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"rotate.sh failed with exit code {result.returncode}. stderr: {result.stderr}"

    archive_file = "/home/user/app/logs/server.log.archive"
    assert os.path.isfile(archive_file), f"Archive file {archive_file} was not created."

    status_file = "/home/user/app/rotation_status.txt"
    assert os.path.isfile(status_file), f"Status file {status_file} was not created."

    with open(status_file, "r") as f:
        status_content = f.read()
    assert "ROTATION_COMPLETE" in status_content, f"String 'ROTATION_COMPLETE' not found in {status_file}"