# test_final_state.py

import os
import subprocess
import time
import pytest

def test_backend_port_extracted():
    path = "/home/user/deploy/backend_port.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == "8443", f"Expected backend_port.txt to contain '8443', but got '{content}'."

def test_symlinks_exist():
    backend_link = "/home/user/deploy/bin/backend_app"
    proxy_link = "/home/user/deploy/bin/proxy_app"

    assert os.path.islink(backend_link), f"{backend_link} is not a symlink."
    assert os.path.islink(proxy_link), f"{proxy_link} is not a symlink."

    backend_target = os.path.realpath(backend_link)
    proxy_target = os.path.realpath(proxy_link)

    assert backend_target == "/home/user/migration/src/backend_app", f"Backend symlink points to {backend_target} instead of /home/user/migration/src/backend_app."
    assert proxy_target == "/home/user/migration/src/proxy_app", f"Proxy symlink points to {proxy_target} instead of /home/user/migration/src/proxy_app."

def test_acls_set_correctly():
    path = "/home/user/deploy/logs/"
    assert os.path.isdir(path), f"Directory {path} does not exist."

    result = subprocess.run(["getfacl", path], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run getfacl."

    output = result.stdout
    assert "group:users:r-x" in output, "ACL group:users:r-x not found on logs directory."
    assert "default:group:users:r--" in output, "Default ACL default:group:users:r-- not found on logs directory."

def test_processes_running():
    # Check backend_app
    backend_running = False
    proxy_running = False

    ps_result = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True)
    for line in ps_result.stdout.splitlines():
        if "backend_app" in line and "8443" in line and "manage.sh" not in line and "grep" not in line:
            backend_running = True
        if "proxy_app" in line and "8080" in line and "8443" in line and "manage.sh" not in line and "grep" not in line:
            proxy_running = True

    assert backend_running, "backend_app is not running with argument 8443."
    assert proxy_running, "proxy_app is not running with arguments 8080 8443."

def test_manage_script_stop():
    script_path = "/home/user/deploy/manage.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Run stop
    subprocess.run([script_path, "stop"], check=False)
    time.sleep(1)

    backend_running = False
    proxy_running = False

    ps_result = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True)
    for line in ps_result.stdout.splitlines():
        if "backend_app" in line and "8443" in line and "manage.sh" not in line and "grep" not in line:
            backend_running = True
        if "proxy_app" in line and "8080" in line and "8443" in line and "manage.sh" not in line and "grep" not in line:
            proxy_running = True

    assert not backend_running, "backend_app is still running after manage.sh stop."
    assert not proxy_running, "proxy_app is still running after manage.sh stop."

    assert not os.path.exists("/home/user/deploy/run/backend.pid"), "backend.pid was not deleted."
    assert not os.path.exists("/home/user/deploy/run/proxy.pid"), "proxy.pid was not deleted."