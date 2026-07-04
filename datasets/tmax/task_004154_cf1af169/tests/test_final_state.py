# test_final_state.py
import os
import stat
import json
import time
import subprocess
import urllib.request
import urllib.error
import pytest

APP_DIR = "/home/user/app"
WAF_PATH = os.path.join(APP_DIR, "waf.py")
NGINX_CONF = os.path.join(APP_DIR, "nginx.conf")
START_SH = os.path.join(APP_DIR, "start_services.sh")
CLEAN_CORPUS = "/home/user/corpus/clean"
EVIL_CORPUS = "/home/user/corpus/evil"

@pytest.fixture(scope="session", autouse=True)
def start_services():
    # Attempt to gracefully kill existing services to avoid port conflicts
    subprocess.run(["pkill", "-f", "nginx"], check=False)
    subprocess.run(["pkill", "-f", "redis-server"], check=False)
    subprocess.run(["pkill", "-f", "api.py"], check=False)
    subprocess.run(["pkill", "-f", "waf.py"], check=False)
    time.sleep(1)

    # Run the startup script to bring up the stack
    subprocess.Popen(["bash", START_SH], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Wait for services to initialize
    time.sleep(3)
    yield

def test_waf_permissions():
    assert os.path.exists(WAF_PATH), f"WAF script {WAF_PATH} does not exist."
    st = os.stat(WAF_PATH)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o700, f"Expected {WAF_PATH} to have 700 permissions, got {oct(perms)}."

def test_nginx_config_updated():
    with open(NGINX_CONF, 'r') as f:
        content = f.read()
    assert "proxy_pass http://127.0.0.1:8081;" in content, "nginx.conf was not updated to proxy to the WAF on port 8081."

def test_startup_script_updated():
    with open(START_SH, 'r') as f:
        content = f.read()
    assert "api.py" in content and "8082" in content, "start_services.sh does not start api.py on the correct port 8082."
    assert "waf.py" in content, "start_services.sh does not start waf.py."

def send_request(payload):
    req = urllib.request.Request(
        "http://127.0.0.1:8080/process",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None

def test_clean_corpus():
    clean_files = [f for f in os.listdir(CLEAN_CORPUS) if f.endswith('.json')]
    assert len(clean_files) > 0, "Clean corpus directory is empty."

    failed = []
    for fname in clean_files:
        with open(os.path.join(CLEAN_CORPUS, fname), 'r') as f:
            payload = json.load(f)
        status = send_request(payload)
        if status != 200:
            failed.append(fname)

    assert not failed, f"{len(failed)} of {len(clean_files)} clean payloads modified/rejected (expected HTTP 200). Offending files: {', '.join(failed[:10])}"

def test_evil_corpus():
    evil_files = [f for f in os.listdir(EVIL_CORPUS) if f.endswith('.json')]
    assert len(evil_files) > 0, "Evil corpus directory is empty."

    failed = []
    for fname in evil_files:
        with open(os.path.join(EVIL_CORPUS, fname), 'r') as f:
            payload = json.load(f)
        status = send_request(payload)
        if status != 403:
            failed.append(fname)

    assert not failed, f"{len(failed)} of {len(evil_files)} evil payloads bypassed (expected HTTP 403). Offending files: {', '.join(failed[:10])}"