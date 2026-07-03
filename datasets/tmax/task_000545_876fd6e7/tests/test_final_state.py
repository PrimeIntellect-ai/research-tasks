# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_url():
    versions = ["v1", "v2", "v3"]
    version = random.choice(versions)
    path_len = random.randint(3, 10)
    path_str = "".join(random.choices(string.ascii_lowercase, k=path_len))

    token_len = random.randint(4, 15)
    token_str = "".join(random.choices(string.ascii_letters + string.digits, k=token_len))

    url = f"/api/{version}/{path_str}?token={token_str}"

    if random.random() > 0.5:
        user_len = random.randint(3, 8)
        user_str = "".join(random.choices(string.ascii_lowercase, k=user_len))
        url += f"&user={user_str}"

    if random.random() > 0.5:
        id_len = random.randint(1, 5)
        id_str = "".join(random.choices(string.digits, k=id_len))
        url += f"&id={id_str}"

    return url

def test_fuzz_equivalence():
    agent_bin = "/home/user/secure_router/target/release/url_processor"
    oracle_bin = "/app/oracle_processor"

    assert os.path.isfile(agent_bin), f"Agent binary not found at {agent_bin}. Did you run 'cargo build --release'?"
    assert os.path.isfile(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    random.seed(1337)
    N = 1000

    for i in range(N):
        url = generate_url()

        agent_proc = subprocess.run([agent_bin, url], capture_output=True, text=True)
        oracle_proc = subprocess.run([oracle_bin, url], capture_output=True, text=True)

        # We only care about stdout matching exactly, as specified in the rules
        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Mismatch on input URL: {url}\n"
            f"Expected (Oracle): {oracle_proc.stdout!r}\n"
            f"Got (Agent): {agent_proc.stdout!r}"
        )