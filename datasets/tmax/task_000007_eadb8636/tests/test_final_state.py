# test_final_state.py
import os
import subprocess
import pytest
import numpy as np

ORACLE_PATH = "/app/cleaner_oracle"
AGENT_PATH = "/home/user/cleaner"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary {AGENT_PATH} not found. Did you compile your C code?"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    np.random.seed(1337)

    num_tests = 50
    for i in range(num_tests):
        # Length ranging from 0 to 100,000 integers
        length = np.random.randint(0, 100001)

        if length > 0:
            # Generate uniformly distributed 32-bit signed integers
            arr = np.random.randint(np.iinfo(np.int32).min, np.iinfo(np.int32).max, size=length, dtype=np.int32)

            # Inject the special value -9999 occasionally to ensure that logic is tested
            inject_mask = np.random.rand(length) < 0.05
            arr[inject_mask] = -9999

            input_bytes = arr.tobytes()
        else:
            input_bytes = b""

        oracle_proc = subprocess.run([ORACLE_PATH], input=input_bytes, capture_output=True)
        agent_proc = subprocess.run([AGENT_PATH], input=input_bytes, capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on test case {i}."
        assert agent_proc.returncode == 0, f"Agent program failed with return code {agent_proc.returncode} on test case {i}."

        if oracle_proc.stdout != agent_proc.stdout:
            # Find the first differing byte to provide a helpful error message
            oracle_out = oracle_proc.stdout
            agent_out = agent_proc.stdout

            min_len = min(len(oracle_out), len(agent_out))
            diff_idx = -1
            for j in range(min_len):
                if oracle_out[j] != agent_out[j]:
                    diff_idx = j
                    break

            if diff_idx == -1:
                diff_idx = min_len

            element_idx = diff_idx // 4

            pytest.fail(
                f"Mismatch on test case {i} (input length {length} integers).\n"
                f"Outputs differ starting at byte index {diff_idx} (corresponding to input integer index {element_idx}).\n"
                f"Oracle output length: {len(oracle_out)} bytes.\n"
                f"Agent output length: {len(agent_out)} bytes."
            )