# test_final_state.py

import os
import random
import string
import base64
import subprocess
import pytest

AGENT_BIN = "/home/user/filter_bin"
ORACLE_BIN = "/app/proxy_oracle"

def test_directories_and_symlink():
    logs_dir = "/home/user/edge_deploy/logs"
    conf_dir = "/home/user/edge_deploy/conf"
    bin_dir = "/home/user/edge_deploy/bin"

    assert os.path.isdir(logs_dir), f"Directory missing: {logs_dir}"
    assert os.path.isdir(conf_dir), f"Directory missing: {conf_dir}"
    assert os.path.isdir(bin_dir), f"Directory missing: {bin_dir}"

    symlink_path = "/home/user/edge_deploy/bin/filter_bin"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink"

    target = os.readlink(symlink_path)
    assert target == "/home/user/filter_bin", f"Symlink {symlink_path} points to {target} instead of /home/user/filter_bin"

def test_fuzz_equivalence():
    assert os.path.isfile(AGENT_BIN), f"Agent binary missing at {AGENT_BIN}"
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary not executable at {AGENT_BIN}"

    random.seed(42)
    printable = string.printable.encode('ascii')

    # We will generate 5000 inputs as specified
    # To ensure we also hit some specific logic branches in the oracle, we will inject 
    # some known patterns into the random generation, but still adhere to the distribution.

    patterns = [
        b"ssh-rsa root",
        b"GET /api/v1/status",
        b"admin " + b"A" * 25,
        b"just some random text"
    ]

    for i in range(5000):
        length = random.randint(0, 100)

        if random.random() < 0.5:
            # 50% valid base64 encoded printable ASCII
            if random.random() < 0.2 and length > 20:
                # Inject some patterns to ensure rules are hit
                raw = random.choice(patterns)
            else:
                raw = bytes(random.choice(printable) for _ in range(length))
            inp = base64.b64encode(raw)
        else:
            # 50% random corrupted base64 or raw bytes
            inp = bytes(random.randint(0, 255) for _ in range(length))

        # Run oracle
        proc_oracle = subprocess.run([ORACLE_BIN], input=inp, capture_output=True)
        # Run agent
        proc_agent = subprocess.run([AGENT_BIN], input=inp, capture_output=True)

        assert proc_oracle.stdout == proc_agent.stdout, (
            f"Output mismatch on input {inp!r}.\n"
            f"Oracle stdout: {proc_oracle.stdout!r}\n"
            f"Agent stdout: {proc_agent.stdout!r}"
        )