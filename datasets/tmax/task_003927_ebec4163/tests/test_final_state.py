# test_final_state.py

import os
import subprocess
import random
import pytest

def test_backup_profile():
    profile_path = "/home/user/.backup_profile"
    assert os.path.exists(profile_path), f"Missing {profile_path}"

    # Check variables
    out = subprocess.check_output(
        f"bash -c 'source {profile_path} && echo $BACKUP_MODE'", shell=True
    ).decode().strip()
    assert out == "RESTORE", f"BACKUP_MODE is '{out}', expected 'RESTORE'"

    out2 = subprocess.check_output(
        f"bash -c 'source {profile_path} && echo $ARCHIVE_ROOT'", shell=True
    ).decode().strip()
    assert out2 == "/tmp/restores", f"ARCHIVE_ROOT is '{out2}', expected '/tmp/restores'"

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.exists(conf_path), f"Missing {conf_path}"

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "/home/user/restore.log" in content, "logrotate.conf does not target /home/user/restore.log"

    # Run logrotate in debug mode to parse the config
    result = subprocess.run(["logrotate", "-d", conf_path], capture_output=True, text=True)
    # logrotate debug output might go to stderr or stdout
    output = result.stdout + result.stderr

    assert result.returncode == 0, f"logrotate failed to parse config: {output}"

    # We can also check the file contents directly for keywords
    assert "daily" in content, "logrotate.conf missing 'daily'"
    assert "rotate 7" in content, "logrotate.conf missing 'rotate 7'"
    assert "compress" in content, "logrotate.conf missing 'compress'"
    assert "10M" in content and ("size" in content or "maxsize" in content), "logrotate.conf missing size 10M directive"

def test_wrapper_script():
    wrapper_path = "/home/user/restore_wrapper.sh"
    assert os.path.exists(wrapper_path), f"Missing {wrapper_path}"
    assert os.access(wrapper_path, os.X_OK), f"{wrapper_path} is not executable"

def generate_fuzz_input(size):
    # First byte is XOR key
    key = random.randint(0, 255)
    data = bytearray([key])

    # Generate RLE stream
    while len(data) < size:
        if random.random() < 0.3:
            # RLE sequence
            count = random.randint(1, 255)
            val = random.randint(0, 255)
            data.extend([0xAA, count, val])
        else:
            # Literal byte
            val = random.randint(0, 255)
            if val == 0xAA:
                data.extend([0xAA, 1, 0xAA])
            else:
                data.append(val)

    return bytes(data[:size])

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_decode"
    agent_path = "/home/user/new_decode"

    assert os.path.exists(agent_path), f"Missing agent executable: {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent executable is not executable: {agent_path}"

    random.seed(42)

    N = 1000
    for i in range(N):
        # vary size between 10 and 10000 bytes for test speed, occasionally larger
        if i % 100 == 0:
            size = random.randint(10000, 100000)
        else:
            size = random.randint(10, 1000)

        test_input = generate_fuzz_input(size)

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path], input=test_input, capture_output=True, timeout=2
            )
            oracle_out = oracle_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle timed out")

        # Run agent
        try:
            agent_proc = subprocess.run(
                [agent_path], input=test_input, capture_output=True, timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail("Agent timed out")

        assert agent_out == oracle_out, f"Mismatch on iteration {i} with input size {len(test_input)}"