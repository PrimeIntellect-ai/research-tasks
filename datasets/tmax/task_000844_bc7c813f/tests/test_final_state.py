# test_final_state.py

import os
import subprocess
import pytest
import random
import struct

ORACLE_PATH = "/app/bin/legacy_tracker"
AGENT_PATH = "/home/user/tracker/new_tracker"

def generate_trkv(seed):
    rng = random.Random(seed)
    out = bytearray(b"TRKV")
    file_count = rng.randint(0, 10)
    out.extend(struct.pack("<H", file_count))

    for _ in range(file_count):
        filename_len = rng.randint(1, 20)
        filename = "".join(rng.choices("abcdefghijklmnopqrstuvwxyz0123456789_.", k=filename_len))
        out.extend(struct.pack("B", filename_len))
        out.extend(filename.encode("ascii"))

        content_len = rng.randint(0, 500)
        content = bytearray()
        while len(content) < content_len:
            choice = rng.random()
            if choice < 0.05:
                pass_len = rng.randint(1, 10)
                pass_str = "PASS=" + "".join(rng.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=pass_len))
                content.extend(pass_str.encode("ascii"))
            elif choice < 0.10:
                content.extend(b"\r\n")
            else:
                content.append(rng.choice(b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 \t\n!@#$%^&*()"))

        content = content[:content_len]
        out.extend(struct.pack("<I", content_len))
        out.extend(content)

    return bytes(out)

def test_fuzz_equivalence():
    assert os.path.exists(AGENT_PATH), f"Agent program missing at {AGENT_PATH}. Did you compile it?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent program not executable at {AGENT_PATH}."

    for i in range(100):
        input_data = generate_trkv(i)

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_data, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_data, capture_output=True)

        assert oracle_proc.returncode == agent_proc.returncode, f"Return code mismatch on seed {i}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        if oracle_proc.stdout != agent_proc.stdout:
            mismatch_idx = -1
            for j in range(min(len(oracle_proc.stdout), len(agent_proc.stdout))):
                if oracle_proc.stdout[j] != agent_proc.stdout[j]:
                    mismatch_idx = j
                    break
            if mismatch_idx == -1:
                mismatch_idx = min(len(oracle_proc.stdout), len(agent_proc.stdout))

            pytest.fail(f"Output mismatch on seed {i}.\n"
                        f"Oracle output length: {len(oracle_proc.stdout)} bytes\n"
                        f"Agent output length: {len(agent_proc.stdout)} bytes\n"
                        f"First mismatch at byte index {mismatch_idx}.")