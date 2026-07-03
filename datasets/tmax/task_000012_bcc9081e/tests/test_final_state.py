# test_final_state.py

import os
import random
import subprocess
import tempfile
import pytest

ORACLE_BIN = "/opt/legacy/validator"
AGENT_BIN = "/home/user/new_validator"
CERTS_DIR = "/home/user/certs"

def test_certs_extracted():
    """Verify that the certificates were extracted to the correct directory."""
    assert os.path.exists(CERTS_DIR), f"Directory {CERTS_DIR} does not exist."
    assert os.path.isdir(CERTS_DIR), f"{CERTS_DIR} is not a directory."
    # Check that there is at least one file in the directory
    files = os.listdir(CERTS_DIR)
    assert len(files) > 0, f"No certificates found in {CERTS_DIR}."

def test_agent_binary_exists():
    """Verify that the new validator binary exists and is executable."""
    assert os.path.exists(AGENT_BIN), f"Agent binary {AGENT_BIN} does not exist."
    assert os.path.isfile(AGENT_BIN), f"{AGENT_BIN} is not a file."
    assert os.access(AGENT_BIN, os.X_OK), f"Agent binary {AGENT_BIN} is not executable."

def generate_fuzz_input(rng):
    """Generate a random fuzz input based on the truth distribution."""
    length = rng.randint(10, 500)
    data = bytearray(rng.getrandbits(8) for _ in range(length))

    # 10% chance to include the magic bytes 'CERT'
    if rng.random() < 0.10:
        # Place 'CERT' at the beginning as it's a header
        magic = b"CERT"
        for i in range(min(4, length)):
            data[i] = magic[i]

    return bytes(data)

def run_program(executable, input_path):
    """Run a program with the given input file and return its output and exit code."""
    try:
        result = subprocess.run(
            [executable, input_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=1.0
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, b"", b"Timeout"
    except Exception as e:
        return -2, b"", str(e).encode()

def test_fuzz_equivalence():
    """Fuzz the agent's binary against the oracle to ensure identical behavior."""
    assert os.path.exists(ORACLE_BIN), f"Oracle binary {ORACLE_BIN} missing."
    assert os.path.exists(AGENT_BIN), f"Agent binary {AGENT_BIN} missing."

    rng = random.Random(42)
    N = 10000

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name

    try:
        for i in range(N):
            fuzz_data = generate_fuzz_input(rng)

            with open(tmp_path, "wb") as f:
                f.write(fuzz_data)

            oracle_code, oracle_out, oracle_err = run_program(ORACLE_BIN, tmp_path)
            agent_code, agent_out, agent_err = run_program(AGENT_BIN, tmp_path)

            if oracle_code != agent_code or oracle_out != agent_out or oracle_err != agent_err:
                error_msg = (
                    f"Mismatch on fuzz iteration {i}!\n"
                    f"Input length: {len(fuzz_data)} bytes\n"
                    f"Input hex (first 32 bytes): {fuzz_data[:32].hex()}\n"
                    f"Oracle: exit={oracle_code}, stdout={oracle_out!r}, stderr={oracle_err!r}\n"
                    f"Agent:  exit={agent_code}, stdout={agent_out!r}, stderr={agent_err!r}"
                )
                pytest.fail(error_msg)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)