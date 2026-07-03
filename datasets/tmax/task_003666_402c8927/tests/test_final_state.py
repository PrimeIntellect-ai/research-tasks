# test_final_state.py

import os
import random
import subprocess
import pytest

def generate_fuzz_stream(num_frames=10000, seed=42):
    random.seed(seed)
    stream = bytearray()
    for _ in range(num_frames):
        if random.random() < 0.8:
            # Valid frame
            n = random.randint(1, 20)
            x = random.randint(-5, 5)
            stream.append(n & 0xFF)
            stream.append(x & 0xFF)
            for _ in range(n):
                stream.append(random.randint(-10, 10) & 0xFF)
        else:
            # Truncated frame
            n = 15
            x = random.randint(-5, 5)
            stream.append(n & 0xFF)
            stream.append(x & 0xFF)
            # Truncate: only emit k bytes where k < n
            k = random.randint(0, n - 1)
            for _ in range(k):
                stream.append(random.randint(-10, 10) & 0xFF)
    return bytes(stream)

def test_poly_eval_fuzz_equivalence():
    oracle_path = "/app/bin/oracle_poly"
    agent_path = "/home/user/poly-eval-fixed"

    assert os.path.isfile(oracle_path), f"Oracle binary not found at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent binary not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    fuzz_input = generate_fuzz_stream(num_frames=10000, seed=1337)

    # Run oracle
    try:
        oracle_proc = subprocess.run(
            [oracle_path],
            input=fuzz_input,
            capture_output=True,
            timeout=10,
            check=True
        )
        oracle_output = oracle_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle failed with return code {e.returncode}. stderr: {e.stderr.decode(errors='replace')}")
    except subprocess.TimeoutExpired:
        pytest.fail("Oracle timed out.")

    # Run agent
    try:
        agent_proc = subprocess.run(
            [agent_path],
            input=fuzz_input,
            capture_output=True,
            timeout=10,
            check=True
        )
        agent_output = agent_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent binary failed with return code {e.returncode}. stderr: {e.stderr.decode(errors='replace')}")
    except subprocess.TimeoutExpired:
        pytest.fail("Agent binary timed out (possible deadlock or infinite loop).")

    if agent_output != oracle_output:
        # To provide a helpful error message, let's find the first divergence
        oracle_lines = oracle_output.splitlines()
        agent_lines = agent_output.splitlines()

        diff_idx = -1
        for i in range(min(len(oracle_lines), len(agent_lines))):
            if oracle_lines[i] != agent_lines[i]:
                diff_idx = i
                break

        if diff_idx == -1:
            if len(oracle_lines) != len(agent_lines):
                pytest.fail(f"Output line count mismatch. Oracle has {len(oracle_lines)} lines, agent has {len(agent_lines)} lines.")
            else:
                pytest.fail("Outputs mismatch but lines are identical (possible newline issues).")

        pytest.fail(
            f"Output mismatch at line {diff_idx + 1}.\n"
            f"Expected (Oracle): {oracle_lines[diff_idx].decode(errors='replace')}\n"
            f"Got (Agent):       {agent_lines[diff_idx].decode(errors='replace')}"
        )