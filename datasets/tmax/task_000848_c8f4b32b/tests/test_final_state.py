# test_final_state.py

import os
import sys
import json
import random
import string
import subprocess
import urllib.request
import urllib.error
import ssl
import time
import pytest

ORACLE_PATH = "/app/oracle_verify_header.py"
AGENT_SCRIPT = "/home/user/verify_header.py"
SERVER_SCRIPT = "/home/user/backup_server.py"
ROTATE_SCRIPT = "/home/user/rotate_logs.py"
CERT_PATH = "/home/user/certs/cert.pem"
KEY_PATH = "/home/user/certs/key.pem"
LOG_DIR = "/home/user/logs"
LOG_FILE = os.path.join(LOG_DIR, "restore.log")


def test_fuzz_equivalence():
    """Fuzz verify_header.py against the oracle."""
    assert os.path.isfile(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"

    random.seed(42)
    charset = string.ascii_letters + string.digits

    for _ in range(500):
        length = random.randint(1, 100)
        test_input = "".join(random.choices(charset, k=length))

        oracle_cmd = [sys.executable, ORACLE_PATH, test_input]
        agent_cmd = [sys.executable, AGENT_SCRIPT, test_input]

        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        assert oracle_res.returncode == 0, "Oracle failed"
        assert agent_res.returncode == 0, f"Agent script failed on input {test_input}:\n{agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, (
            f"Output mismatch on input '{test_input}'.\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )


def test_server_files_and_certs():
    """Verify server script and TLS certificates exist."""
    assert os.path.isfile(SERVER_SCRIPT), f"Missing {SERVER_SCRIPT}"
    assert os.path.isfile(CERT_PATH), f"Missing cert at {CERT_PATH}"
    assert os.path.isfile(KEY_PATH), f"Missing key at {KEY_PATH}"


def test_server_health_endpoint():
    """Verify /health endpoint returns HTTP 200 and correct JSON."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = "https://127.0.0.1:8443/health"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
            assert data == {"status": "ok"}, f"Unexpected health response: {data}"
    except Exception as e:
        pytest.fail(f"Failed to connect to {url}: {e}")


def test_server_verify_endpoint_and_logging():
    """Verify /verify endpoint works and logs correctly."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    test_data = "abc"
    expected_output = "111_110_109"
    url = f"https://127.0.0.1:8443/verify?data={test_data}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            out = response.read().decode("utf-8").strip()
            assert out == expected_output, f"Expected {expected_output}, got {out}"
    except Exception as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    # Check log
    assert os.path.isfile(LOG_FILE), f"Log file missing at {LOG_FILE}"
    with open(LOG_FILE, "r") as f:
        log_content = f.read()

    expected_log_snippet = f"VERIFY: {test_data} -> {expected_output}"
    assert expected_log_snippet in log_content, f"Expected log snippet '{expected_log_snippet}' not found in {LOG_FILE}"


def test_log_rotation():
    """Verify rotate_logs.py correctly rotates log files."""
    assert os.path.isfile(ROTATE_SCRIPT), f"Missing {ROTATE_SCRIPT}"

    os.makedirs(LOG_DIR, exist_ok=True)

    # Setup mock logs
    with open(os.path.join(LOG_DIR, "restore.log"), "w") as f: f.write("0")
    with open(os.path.join(LOG_DIR, "restore.log.1"), "w") as f: f.write("1")
    with open(os.path.join(LOG_DIR, "restore.log.2"), "w") as f: f.write("2")
    with open(os.path.join(LOG_DIR, "restore.log.3"), "w") as f: f.write("3")

    res = subprocess.run([sys.executable, ROTATE_SCRIPT], capture_output=True, text=True)
    assert res.returncode == 0, f"rotate_logs.py failed:\n{res.stderr}"

    # Verify rotation
    assert os.path.isfile(os.path.join(LOG_DIR, "restore.log")), "restore.log missing"
    with open(os.path.join(LOG_DIR, "restore.log"), "r") as f: assert f.read() == "", "restore.log should be empty"

    assert os.path.isfile(os.path.join(LOG_DIR, "restore.log.1")), "restore.log.1 missing"
    with open(os.path.join(LOG_DIR, "restore.log.1"), "r") as f: assert f.read() == "0", "restore.log.1 should contain '0'"

    assert os.path.isfile(os.path.join(LOG_DIR, "restore.log.2")), "restore.log.2 missing"
    with open(os.path.join(LOG_DIR, "restore.log.2"), "r") as f: assert f.read() == "1", "restore.log.2 should contain '1'"

    assert os.path.isfile(os.path.join(LOG_DIR, "restore.log.3")), "restore.log.3 missing"
    with open(os.path.join(LOG_DIR, "restore.log.3"), "r") as f: assert f.read() == "2", "restore.log.3 should contain '2'"

    assert not os.path.exists(os.path.join(LOG_DIR, "restore.log.4")), "restore.log.4 should not exist"