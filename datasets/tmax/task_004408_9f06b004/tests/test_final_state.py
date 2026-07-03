# test_final_state.py

import os
import subprocess
import random
import struct
import tempfile
import json
import pytest

AGENT_SCRIPT = "/home/user/fixed_processor.py"
ORACLE_BINARY = "/app/oracle_processor"
NUM_FUZZ_TESTS = 20

def generate_fuzz_wav(path, seed):
    random.seed(seed)

    sample_rate = 44100
    duration = random.uniform(1.0, 5.0)
    num_samples = int(sample_rate * duration)

    is_corrupt = random.random() < 0.5

    with open(path, 'wb') as f:
        f.write(b'RIFF')
        f.write(struct.pack('<I', 36 + num_samples * 2))
        f.write(b'WAVE')

        if is_corrupt and random.random() < 0.5:
            f.write(b'fMt ') # Corrupted header
        else:
            f.write(b'fmt ')

        f.write(struct.pack('<I', 16))
        f.write(struct.pack('<H', 1)) # PCM
        f.write(struct.pack('<H', 1)) # Mono
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', sample_rate * 2))
        f.write(struct.pack('<H', 2))
        f.write(struct.pack('<H', 16))

        if is_corrupt and random.random() < 0.5:
            f.write(b'dAtA') # Corrupted header
        else:
            f.write(b'data')

        f.write(struct.pack('<I', num_samples * 2))

        # Write random data
        chunk_size = 1024 * 1024
        bytes_to_write = num_samples * 2
        while bytes_to_write > 0:
            write_size = min(chunk_size, bytes_to_write)
            f.write(random.randbytes(write_size))
            bytes_to_write -= write_size

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout expired"

def test_fixed_processor_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Fixed script not found at {AGENT_SCRIPT}"

@pytest.mark.parametrize("seed", range(NUM_FUZZ_TESTS))
def test_fuzz_equivalence(seed):
    assert os.path.isfile(ORACLE_BINARY), f"Oracle binary not found at {ORACLE_BINARY}"
    assert os.access(ORACLE_BINARY, os.X_OK), f"Oracle binary is not executable: {ORACLE_BINARY}"

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        wav_path = tmp.name

    try:
        generate_fuzz_wav(wav_path, seed)

        oracle_cmd = [ORACLE_BINARY, wav_path]
        oracle_rc, oracle_out, oracle_err = run_cmd(oracle_cmd)

        agent_cmd = ["/usr/bin/python3", AGENT_SCRIPT, wav_path]
        agent_rc, agent_out, agent_err = run_cmd(agent_cmd)

        # We expect the stdout to match exactly (usually JSON output)
        # Or at least if both fail, they should fail in a similar way, but we will focus on stdout

        error_msg = (
            f"Mismatch on fuzz input seed {seed}.\n"
            f"Oracle output:\n{oracle_out}\n"
            f"Agent output:\n{agent_out}\n"
            f"Oracle stderr:\n{oracle_err}\n"
            f"Agent stderr:\n{agent_err}\n"
        )

        assert oracle_out == agent_out, error_msg

    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)