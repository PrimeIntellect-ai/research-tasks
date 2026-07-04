# test_final_state.py

import os
import time
import struct
import random
import hashlib
import subprocess
import pytest

def generate_test_data(base_path, delta_path, base_size=50*1024*1024, num_ops=15000):
    # Generate random base file
    with open(base_path, 'wb') as f:
        f.write(os.urandom(base_size))

    # Generate delta file
    with open(delta_path, 'wb') as f:
        f.write(b'DLTA')
        for _ in range(num_ops):
            op = random.choices([1, 2, 3], weights=[0.6, 0.2, 0.2])[0]
            if op == 1:  # COPY
                length = random.randint(100, 4000)
                offset = random.randint(0, base_size - length)
                f.write(struct.pack('<BII', 1, offset, length))
            elif op == 2:  # INSERT
                length = random.randint(10, 500)
                data = os.urandom(length)
                f.write(struct.pack('<BI', 2, length))
                f.write(data)
            elif op == 3:  # FILL
                value = random.randint(0, 255)
                length = random.randint(100, 4000)
                f.write(struct.pack('<BBI', 3, value, length))

def get_file_sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def test_fast_apply_speedup_and_correctness(tmp_path):
    script_path = "/home/user/fast_apply.sh"
    orig_binary = "/app/delta_apply"

    assert os.path.exists(script_path), f"Agent script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Agent script {script_path} is not executable"

    base_file = str(tmp_path / "base.bin")
    delta_file = str(tmp_path / "delta.bin")
    out_orig = str(tmp_path / "out_orig.bin")
    out_agent = str(tmp_path / "out_agent.bin")

    # Generate data
    generate_test_data(base_file, delta_file)

    # Run original binary
    t0 = time.time()
    with open(out_orig, 'wb') as f:
        subprocess.run([orig_binary, base_file, delta_file], stdout=f, check=True)
    time_orig = time.time() - t0

    # Run agent script
    t0 = time.time()
    with open(out_agent, 'wb') as f:
        subprocess.run([script_path, base_file, delta_file], stdout=f, check=True)
    time_agent = time.time() - t0

    # Check correctness
    orig_hash = get_file_sha256(out_orig)
    agent_hash = get_file_sha256(out_agent)

    assert orig_hash == agent_hash, (
        f"Output mismatch! Original SHA256: {orig_hash}, Agent SHA256: {agent_hash}"
    )

    # Check speedup
    speedup = time_orig / time_agent
    threshold = 2.5

    assert speedup >= threshold, (
        f"Speedup metric failed: required >= {threshold:.2f}x, "
        f"but got {speedup:.2f}x (Orig: {time_orig:.3f}s, Agent: {time_agent:.3f}s)"
    )