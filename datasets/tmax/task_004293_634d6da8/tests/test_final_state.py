# test_final_state.py

import os
import subprocess
import random
import struct
import time
import pytest

def generate_fuzz_input():
    out = bytearray()
    while len(out) < 1024:
        choice = random.randint(0, 2)
        if choice == 0:
            # Normal log
            ts = random.randint(0, 2**64 - 1)
            metric = random.uniform(-1000.0, 1000.0)
            msg = bytes([random.randint(32, 126) for _ in range(random.randint(0, 50))])
            out += b"LOG1" + struct.pack("<QfH", ts, metric, len(msg)) + msg
        elif choice == 1:
            # WAL log
            crc = random.randint(0, 2**32 - 1)
            out += b"WAL\x01" + struct.pack("<I", crc)
            ts = random.randint(0, 2**64 - 1)
            metric = random.uniform(-1000.0, 1000.0)
            msg = bytes([random.randint(32, 126) for _ in range(random.randint(0, 50))])
            out += b"LOG1" + struct.pack("<QfH", ts, metric, len(msg)) + msg
        else:
            # Garbage
            out += bytes([random.randint(0, 255) for _ in range(random.randint(1, 20))])

        if random.random() < 0.1:
            break

    return bytes(out)[:1024]

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_processor"
    agent_path = "/home/user/services/processor/processor"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"

    random.seed(42)
    for i in range(1000):
        data = generate_fuzz_input()

        oracle_proc = subprocess.run([oracle_path], input=data, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=data, capture_output=True)

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input (hex): {data.hex()}\n"
                f"Oracle stdout: {oracle_proc.stdout!r}\n"
                f"Agent stdout: {agent_proc.stdout!r}\n"
                f"Oracle stderr: {oracle_proc.stderr!r}\n"
                f"Agent stderr: {agent_proc.stderr!r}"
            )

def test_e2e_services():
    script_path = "/home/user/start_services.sh"
    assert os.path.isfile(script_path), f"Startup script not found at {script_path}"

    # Terminate any existing processes just in case
    subprocess.run(["pkill", "-f", "redis-server"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "processor"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "generator"], stderr=subprocess.DEVNULL)
    time.sleep(1)

    proc = subprocess.Popen(["bash", script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        time.sleep(5)

        # Check redis for logs_processed_count
        # We can use redis-cli since it should be installed with redis-server
        res1 = subprocess.run(["redis-cli", "GET", "logs_processed_count"], capture_output=True, text=True)
        val1 = res1.stdout.strip()
        assert val1 and val1 != "(nil)", "logs_processed_count not found in Redis or is nil"

        time.sleep(2)
        res2 = subprocess.run(["redis-cli", "GET", "logs_processed_count"], capture_output=True, text=True)
        val2 = res2.stdout.strip()

        assert int(val2) > int(val1), f"logs_processed_count is not incrementing. Val1: {val1}, Val2: {val2}"
    finally:
        subprocess.run(["pkill", "-P", str(proc.pid)], stderr=subprocess.DEVNULL)
        proc.kill()
        subprocess.run(["pkill", "-f", "redis-server"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "processor"], stderr=subprocess.DEVNULL)
        subprocess.run(["pkill", "-f", "generator"], stderr=subprocess.DEVNULL)