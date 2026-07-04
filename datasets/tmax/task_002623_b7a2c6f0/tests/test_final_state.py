# test_final_state.py

import os
import time
import subprocess
import pytest

def setup_module(module):
    """Ensure the base and override env files exist for the test."""
    base_content = """APP_VERSION=1.0.0
BUILD_THREADS=4
DEBUG=false
PLATFORM=android
"""
    override_content = """DEBUG=true
SIGNING_KEY=prod.keystore
APP_VERSION=1.0.1
"""
    with open('/home/user/config_base.env', 'w') as f:
        f.write(base_content)
    with open('/home/user/config_override.env', 'w') as f:
        f.write(override_content)

def test_scripts_exist_and_executable():
    """Check that the required scripts exist and are executable."""
    assert os.path.isfile('/home/user/ci_backend.sh'), "/home/user/ci_backend.sh does not exist"
    assert os.access('/home/user/ci_backend.sh', os.X_OK), "/home/user/ci_backend.sh is not executable"

    assert os.path.isfile('/home/user/start_server.sh'), "/home/user/start_server.sh does not exist"
    assert os.access('/home/user/start_server.sh', os.X_OK), "/home/user/start_server.sh is not executable"

def test_websocket_server_and_logic():
    """Test the WebSocket server, rate limiting, and expression evaluation."""
    # We use websocat as the client since the task requires installing it
    try:
        p = subprocess.Popen(
            ['websocat', 'ws://127.0.0.1:9090'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
    except FileNotFoundError:
        pytest.fail("websocat is not installed or not in PATH. The task required installing it.")

    try:
        # 1. First valid build
        p.stdin.write("BUILD AppOne 10+5\n")
        p.stdin.flush()
        res1 = p.stdout.readline().strip()
        assert res1 == "ACCEPTED AppOne 15", f"Expected 'ACCEPTED AppOne 15', got '{res1}'"

        # 2. Rate limit trigger (sent immediately after)
        p.stdin.write("BUILD AppTwo 2\n")
        p.stdin.flush()
        res2 = p.stdout.readline().strip()
        assert res2 == "RATE_LIMIT", f"Expected 'RATE_LIMIT', got '{res2}'"

        # 3. Wait for rate limit window to pass (2 seconds required, wait 2.5)
        time.sleep(2.5)

        # 4. Second valid build
        p.stdin.write("BUILD AppThree 2*3\n")
        p.stdin.flush()
        res3 = p.stdout.readline().strip()
        assert res3 == "ACCEPTED AppThree 6", f"Expected 'ACCEPTED AppThree 6', got '{res3}'"

    finally:
        p.terminate()
        p.wait()

def test_ci_states_log():
    """Check that the state machine logs correctly to /home/user/ci_states.log."""
    # Wait for the 1-second simulated build time to finish for the last request
    time.sleep(1.5)

    log_path = '/home/user/ci_states.log'
    assert os.path.isfile(log_path), f"{log_path} does not exist"

    with open(log_path, 'r') as f:
        content = f.read().strip()

    # Check that AppOne and AppThree went through INIT and SUCCESS
    assert "[AppOne] INIT" in content, "[AppOne] INIT not found in ci_states.log"
    assert "[AppOne] SUCCESS" in content, "[AppOne] SUCCESS not found in ci_states.log"
    assert "[AppThree] INIT" in content, "[AppThree] INIT not found in ci_states.log"
    assert "[AppThree] SUCCESS" in content, "[AppThree] SUCCESS not found in ci_states.log"

    # Ensure AppTwo (rate limited) is NOT in the log
    assert "[AppTwo]" not in content, "Rate-limited AppTwo should not appear in ci_states.log"

def test_config_merged_env():
    """Check that the environment variables are correctly merged and sorted."""
    merged_path = '/home/user/config_merged.env'
    assert os.path.isfile(merged_path), f"{merged_path} does not exist"

    with open(merged_path, 'r') as f:
        merged_lines = [line.strip() for line in f if line.strip()]

    expected = [
        "APP_VERSION=1.0.1",
        "BUILD_THREADS=4",
        "DEBUG=true",
        "PLATFORM=android",
        "SIGNING_KEY=prod.keystore"
    ]

    assert merged_lines == expected, f"Merged config mismatch.\nExpected: {expected}\nGot: {merged_lines}"