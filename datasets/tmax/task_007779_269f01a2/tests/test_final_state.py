# test_final_state.py
import os
import stat
import subprocess
import re
import pytest

SCRIPT_DIR = "/home/user"
DATA_VOLUME = "/home/user/data_volume"
ROUTES_CONF = "/home/user/routes.conf"
ROUTER_LOG = "/home/user/router.log"

def get_script_path():
    for ext in ['sh', 'py']:
        path = os.path.join(SCRIPT_DIR, f"storage_router.{ext}")
        if os.path.exists(path):
            return path
    return None

def test_script_exists_and_executable():
    script_path = get_script_path()
    assert script_path is not None, "storage_router script not found in /home/user"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable"

def test_crontab_exists():
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        pytest.fail("crontab for user does not exist or failed to load")

    match = re.search(r"\*/5\s+\*\s+\*\s+\*\s+\*\s+.+storage_router\.(sh|py)", output)
    assert match is not None, "Cron job for storage_router running every 5 minutes not found in crontab"

def create_dummy_file(size_mb, filename):
    filepath = os.path.join(DATA_VOLUME, filename)
    with open(filepath, "wb") as f:
        f.write(b'\0' * (size_mb * 1024 * 1024))
    return filepath

def get_log_lines():
    if not os.path.exists(ROUTER_LOG):
        return []
    with open(ROUTER_LOG, "r") as f:
        return f.readlines()

def test_script_behavior():
    script_path = get_script_path()
    if not script_path:
        pytest.fail("Script not found")

    # Clean up before testing
    if os.path.exists(ROUTES_CONF):
        os.remove(ROUTES_CONF)
    if os.path.exists(ROUTER_LOG):
        os.remove(ROUTER_LOG)
    for f in os.listdir(DATA_VOLUME):
        os.remove(os.path.join(DATA_VOLUME, f))

    # Test <= 50MB
    create_dummy_file(10, "test1.dat")
    subprocess.run([script_path], check=True)

    assert os.path.exists(ROUTES_CONF), "routes.conf was not created"
    with open(ROUTES_CONF, "r") as f:
        content = f.read().strip()
    assert content == "10.0.0.0/24 via 192.168.1.1 dev eth0", "routes.conf content is incorrect for <= 50MB"

    log_lines = get_log_lines()
    assert len(log_lines) == 1, "Expected exactly 1 log line after first run"
    assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] ROUTE_CHANGED: 192\.168\.1\.1", log_lines[0]), "Log format incorrect for <= 50MB"

    # Test Idempotency for <= 50MB
    subprocess.run([script_path], check=True)
    log_lines_after = get_log_lines()
    assert len(log_lines_after) == 1, "Script is not idempotent; it appended to the log when state didn't change"

    # Test > 50MB
    create_dummy_file(45, "test2.dat") # Total 55MB
    subprocess.run([script_path], check=True)

    with open(ROUTES_CONF, "r") as f:
        content = f.read().strip()
    assert content == "10.0.0.0/24 via 192.168.2.254 dev eth1", "routes.conf content is incorrect for > 50MB"

    log_lines = get_log_lines()
    assert len(log_lines) == 2, "Expected exactly 2 log lines after second state change"
    assert re.search(r"\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] ROUTE_CHANGED: 192\.168\.2\.254", log_lines[1]), "Log format incorrect for > 50MB"

    # Test Idempotency for > 50MB
    subprocess.run([script_path], check=True)
    log_lines_after = get_log_lines()
    assert len(log_lines_after) == 2, "Script is not idempotent; it appended to the log when state didn't change"