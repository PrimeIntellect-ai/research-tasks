# test_final_state.py
import os
import subprocess
import random

def test_secure_parser_fuzz_equivalence():
    oracle_path = "/app/oracle_secure_parser"
    agent_path = "/home/user/secure_parser"
    secret = "2997560681"

    assert os.path.exists(agent_path), f"Agent executable {agent_path} is missing."
    assert os.access(agent_path, os.X_OK), f"Agent executable {agent_path} is not executable."
    assert os.path.exists(oracle_path), f"Oracle executable {oracle_path} is missing."

    random.seed(42)

    # Run N = 10000 fuzzing iterations
    for i in range(10000):
        length = random.randint(0, 8192)

        # Generate completely random bytes for the majority of tests.
        # For a portion of the tests, inject the expected prefix to ensure the "AUTHENTICATED" 
        # code path is also thoroughly fuzzed and verified for equivalence.
        if i < 9000:
            input_data = random.randbytes(length)
        else:
            prefix = f"AUTH-{secret}-".encode('utf-8')
            rem_len = max(0, length - len(prefix))
            input_data = prefix + random.randbytes(rem_len)

        try:
            oracle_proc = subprocess.run(
                [oracle_path, secret],
                input=input_data,
                capture_output=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            assert False, "Oracle timed out."

        try:
            agent_proc = subprocess.run(
                [agent_path, secret],
                input=input_data,
                capture_output=True,
                timeout=2
            )
        except subprocess.TimeoutExpired:
            assert False, f"Agent timed out on input length {len(input_data)}."

        error_msg_base = f"Mismatch on input length {len(input_data)} (Iteration {i})."

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"{error_msg_base} Exit code mismatch. "
            f"Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}."
        )
        assert agent_proc.stdout == oracle_proc.stdout, (
            f"{error_msg_base} Stdout mismatch. "
            f"Oracle: {oracle_proc.stdout!r}, Agent: {agent_proc.stdout!r}."
        )
        assert agent_proc.stderr == oracle_proc.stderr, (
            f"{error_msg_base} Stderr mismatch. "
            f"Oracle: {oracle_proc.stderr!r}, Agent: {agent_proc.stderr!r}."
        )