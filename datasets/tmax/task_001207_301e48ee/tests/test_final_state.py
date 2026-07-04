# test_final_state.py

import os
import sys
import subprocess
import random
import struct
import tempfile
import pytest

AGENT_SCRIPT = "/home/user/parser.py"
ORACLE_SCRIPT = "/app/oracle_parser"

def generate_random_dsar(file_path, seed):
    rng = random.Random(seed)
    num_records = rng.randint(0, 50)

    with open(file_path, "wb") as f:
        # Header
        f.write(b"DSAR")
        f.write(struct.pack("<H", num_records))

        charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/.-_"

        for _ in range(num_records):
            path_len = rng.randint(1, 255)

            # Generate path
            is_malicious = rng.random() < 0.3
            if is_malicious:
                malicious_type = rng.choice(["starts_with_slash", "contains_dotdot"])
                if malicious_type == "starts_with_slash":
                    path = "/" + "".join(rng.choice(charset) for _ in range(path_len - 1))
                else:
                    if path_len < 3:
                        path_len = 3
                    insert_idx = rng.randint(0, path_len - 3)
                    prefix = "".join(rng.choice(charset) for _ in range(insert_idx))
                    suffix = "".join(rng.choice(charset) for _ in range(path_len - 3 - insert_idx))
                    path = prefix + "../" + suffix
            else:
                path = "".join(rng.choice(charset) for _ in range(path_len))
                # Ensure it doesn't accidentally become malicious
                path = path.lstrip("/")
                path = path.replace("../", "X./")
                if len(path) == 0:
                    path = "a"
                path_len = len(path)

            path_bytes = path.encode("ascii")

            offset = rng.randint(0, 1000000)
            size = rng.randint(0, 10000)
            crc = rng.randint(0, 0xFFFFFFFF)

            f.write(struct.pack("<B", path_len))
            f.write(path_bytes)
            f.write(struct.pack("<QQI", offset, size, crc))

def test_agent_script_exists_and_executable():
    assert os.path.exists(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_SCRIPT), f"Oracle script {ORACLE_SCRIPT} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(50):
            dsar_path = os.path.join(tmpdir, f"test_{i}.dsar")
            generate_random_dsar(dsar_path, seed=42+i)

            # Run oracle
            oracle_cmd = [ORACLE_SCRIPT, dsar_path]
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)

            # Run agent
            agent_cmd = [AGENT_SCRIPT, dsar_path]
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

            assert agent_res.returncode == oracle_res.returncode, (
                f"Return code mismatch on input {i}.\n"
                f"Oracle return code: {oracle_res.returncode}\n"
                f"Agent return code: {agent_res.returncode}\n"
                f"Oracle stderr: {oracle_res.stderr}\n"
                f"Agent stderr: {agent_res.stderr}"
            )

            assert agent_res.stdout == oracle_res.stdout, (
                f"Output mismatch on input {i} (seed {42+i}).\n"
                f"Oracle output:\n{oracle_res.stdout}\n"
                f"Agent output:\n{agent_res.stdout}\n"
            )

def test_mmap_usage():
    with open(AGENT_SCRIPT, "r") as f:
        content = f.read()
    assert "mmap" in content, "The agent script must use the 'mmap' module."