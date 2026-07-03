# test_final_state.py

import os
import subprocess
import random
import pytest

ORACLE_PATH = "/app/legacy_feature_extractor"
AGENT_SCRIPT = "/home/user/py_feature_extractor.py"
N_ITERATIONS = 100
SEED = 42

def test_agent_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    random.seed(SEED)

    for i in range(N_ITERATIONS):
        # Generate sequence of 1 to 5000 floats between -100.0 and 100.0
        seq_length = random.randint(1, 5000)
        input_floats = [random.uniform(-100.0, 100.0) for _ in range(seq_length)]
        input_data = "\n".join(f"{x:.6f}" for x in input_floats) + "\n"
        input_bytes = input_data.encode('utf-8')

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [ORACLE_PATH],
                input=input_bytes,
                capture_output=True,
                check=True,
                timeout=5
            )
            oracle_output = oracle_proc.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on iteration {i}: {e.stderr.decode('utf-8')}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Oracle timed out on iteration {i}")

        # Run agent script
        try:
            agent_proc = subprocess.run(
                ["python3", AGENT_SCRIPT],
                input=input_bytes,
                capture_output=True,
                check=True,
                timeout=5
            )
            agent_output = agent_proc.stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on iteration {i}: {e.stderr.decode('utf-8')}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent script timed out on iteration {i}")

        # Compare outputs
        if oracle_output != agent_output:
            # Truncate output for error message if too long
            err_msg = f"Output mismatch on iteration {i} (sequence length {seq_length}).\n"

            # Show the first few lines of mismatch
            oracle_lines = oracle_output.splitlines()
            agent_lines = agent_output.splitlines()

            for line_idx, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
                if o_line != a_line:
                    err_msg += f"First mismatch at line {line_idx}:\n"
                    err_msg += f"Input value: {input_floats[line_idx]:.6f}\n"
                    err_msg += f"Expected (Oracle): {o_line}\n"
                    err_msg += f"Got (Agent):      {a_line}\n"
                    break
            else:
                if len(oracle_lines) != len(agent_lines):
                    err_msg += f"Line count mismatch. Oracle: {len(oracle_lines)}, Agent: {len(agent_lines)}\n"

            pytest.fail(err_msg)