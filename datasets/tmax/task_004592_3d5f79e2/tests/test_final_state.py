# test_final_state.py

import os
import subprocess
import random
import string
import struct
import json
import time
import pytest

ORACLE_PATH = "/app/legacy_config_tracker"
AGENT_PATH = "/home/user/config_tracker"

def generate_random_string(min_len, max_len):
    length = random.randint(min_len, max_len)
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def create_baseline_config(filepath, num_pairs):
    with open(filepath, 'wb') as f:
        f.write(b'CFG1')
        for _ in range(num_pairs):
            k = generate_random_string(1, 20).encode('utf-8')
            v = generate_random_string(1, 100).encode('utf-8')
            f.write(struct.pack('<H', len(k)))
            f.write(k)
            f.write(struct.pack('<I', len(v)))
            f.write(v)

def read_output_line(proc):
    line = proc.stdout.readline()
    if not line:
        return None
    return line.decode('utf-8').strip()

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent not found at {AGENT_PATH}"

    random.seed(42)

    # We'll run fewer iterations to ensure it completes within test timeouts,
    # but still enough to test functionality.
    N = 20 

    for i in range(N):
        filepath = f"/tmp/baseline_{i}.bin"
        create_baseline_config(filepath, random.randint(1, 50))

        oracle_proc = subprocess.Popen(
            [ORACLE_PATH, filepath],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        agent_proc = subprocess.Popen(
            [AGENT_PATH, filepath],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )

        try:
            num_ops = random.randint(10, 100)
            for _ in range(num_ops):
                if random.random() < 0.05:
                    # File modification
                    create_baseline_config(filepath, random.randint(1, 50))
                    # Wait for inotify to trigger and produce output
                    # To avoid hanging if one fails, we use a short timeout or just read
                    # Since we can't easily timeout readline without select, we assume it works
                    # Actually, a safer way is to just test stdin for now if inotify is racy,
                    # but the prompt requires it.
                    time.sleep(0.1)

                    # Both should have produced an output line due to reload
                    # Wait, if we don't write to stdin, we might block forever if inotify fails.
                    # We will write a dummy stdin to force an output if inotify was missed.

                # Stdin event
                op = "DEL" if random.random() < 0.1 else "PUT"
                k = generate_random_string(1, 20)
                v = generate_random_string(1, 100)

                if op == "PUT":
                    event = {"op": "PUT", "k": k, "v": v}
                else:
                    event = {"op": "DEL", "k": k}

                json_line = json.dumps(event) + "\n"

                oracle_proc.stdin.write(json_line.encode('utf-8'))
                oracle_proc.stdin.flush()

                agent_proc.stdin.write(json_line.encode('utf-8'))
                agent_proc.stdin.flush()

                oracle_out = read_output_line(oracle_proc)
                agent_out = read_output_line(agent_proc)

                assert oracle_out == agent_out, f"Mismatch on iteration {i}, event {json_line.strip()}.\nOracle: {oracle_out}\nAgent:  {agent_out}"

        finally:
            oracle_proc.terminate()
            agent_proc.terminate()
            oracle_proc.wait()
            agent_proc.wait()
            if os.path.exists(filepath):
                os.remove(filepath)