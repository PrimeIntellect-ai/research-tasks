# test_final_state.py

import urllib.request
import urllib.error
import json
import os
import subprocess
import time
import pytest

EVIL_DIR = "/home/user/data/evil"
CLEAN_DIR = "/home/user/data/clean"
URL = "http://localhost:5000/submit"

@pytest.fixture(scope="session", autouse=True)
def setup_services():
    """
    Ensure the build is completed and the services are running,
    as specified in the verification test description.
    """
    build_script = "/home/user/app/build.sh"
    if os.path.exists(build_script):
        subprocess.run(["bash", build_script], cwd="/home/user/app", check=False)

    start_script = "/home/user/app/start.sh"
    config_env = "/home/user/app/config.env"
    if os.path.exists(start_script) and os.path.exists(config_env):
        cmd = f"source {config_env} && bash {start_script}"
        subprocess.run(cmd, shell=True, cwd="/home/user/app", executable="/bin/bash")

    # Allow some time for Redis and Flask to initialize
    time.sleep(3)

def check_payload(text):
    data = json.dumps({"text": text}).encode('utf-8')
    req = urllib.request.Request(URL, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return None

def test_adversarial_corpus():
    assert os.path.isdir(EVIL_DIR), f"Directory {EVIL_DIR} is missing"
    assert os.path.isdir(CLEAN_DIR), f"Directory {CLEAN_DIR} is missing"

    evil_files = sorted([f for f in os.listdir(EVIL_DIR) if os.path.isfile(os.path.join(EVIL_DIR, f))])
    clean_files = sorted([f for f in os.listdir(CLEAN_DIR) if os.path.isfile(os.path.join(CLEAN_DIR, f))])

    assert len(evil_files) > 0, "No evil files found to test."
    assert len(clean_files) > 0, "No clean files found to test."

    evil_bypassed = []
    clean_modified = []

    for f in evil_files:
        with open(os.path.join(EVIL_DIR, f), 'r', encoding='utf-8') as file:
            content = file.read()
        status = check_payload(content)
        if status != 403:
            evil_bypassed.append(f)

    for f in clean_files:
        with open(os.path.join(CLEAN_DIR, f), 'r', encoding='utf-8') as file:
            content = file.read()
        status = check_payload(content)
        if status != 200:
            clean_modified.append(f)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed[:10])}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified[:10])}")

    if error_msg:
        pytest.fail("\n".join(error_msg))