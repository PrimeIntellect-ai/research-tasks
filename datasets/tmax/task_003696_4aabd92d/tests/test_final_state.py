# test_final_state.py

import os
import struct
import random
import subprocess
import pytest

AGENT_PROGRAM = "/home/user/recommend"
ORACLE_PROGRAM = "/app/oracle_recommend"

def test_agent_program_exists_and_executable():
    assert os.path.exists(AGENT_PROGRAM), f"Agent program missing at {AGENT_PROGRAM}"
    assert os.path.isfile(AGENT_PROGRAM), f"Path {AGENT_PROGRAM} is not a file"
    assert os.access(AGENT_PROGRAM, os.X_OK), f"Agent program at {AGENT_PROGRAM} is not executable"

def generate_fuzz_input(seed):
    random.seed(seed)
    N = random.randint(1, 1000)
    Q = random.randint(1, 1000)

    data = bytearray()
    data.extend(struct.pack("<I", N))

    for _ in range(N + Q):
        f1 = random.uniform(0.0, 255.0)
        f2 = random.uniform(0.0, 255.0)
        f3 = random.uniform(0.0, 255.0)
        f4 = random.uniform(0.0, 255.0)
        data.extend(struct.pack("<ffff", f1, f2, f3, f4))

    return bytes(data), N, Q

def run_program(executable, input_data):
    try:
        result = subprocess.run(
            [executable],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
            check=True
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        pytest.fail(f"Execution of {executable} timed out.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {executable} failed with return code {e.returncode}.\nStderr: {e.stderr.decode('utf-8', errors='ignore')}")

@pytest.mark.parametrize("seed", range(100))
def test_fuzz_equivalence(seed):
    input_data, N, Q = generate_fuzz_input(seed)

    oracle_output = run_program(ORACLE_PROGRAM, input_data)
    agent_output = run_program(AGENT_PROGRAM, input_data)

    expected_output_size = Q * 4

    assert len(oracle_output) == expected_output_size, f"Oracle output size mismatch. Expected {expected_output_size}, got {len(oracle_output)}"

    if agent_output != oracle_output:
        # Unpack outputs for better error message
        try:
            oracle_vals = struct.unpack(f"<{Q}I", oracle_output)
        except Exception:
            oracle_vals = "Unparseable oracle output"

        try:
            agent_vals = struct.unpack(f"<{len(agent_output)//4}I", agent_output)
        except Exception:
            agent_vals = "Unparseable agent output"

        pytest.fail(
            f"Output mismatch on fuzz iteration with seed {seed} (N={N}, Q={Q}).\n"
            f"Oracle output (first 10): {oracle_vals[:10] if isinstance(oracle_vals, tuple) else oracle_vals}\n"
            f"Agent output (first 10): {agent_vals[:10] if isinstance(agent_vals, tuple) else agent_vals}"
        )