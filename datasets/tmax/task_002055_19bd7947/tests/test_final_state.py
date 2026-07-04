# test_final_state.py
import os
import random
import string
import subprocess
import pytest

def test_evasion_payload_fuzz_equivalence():
    agent_bin = "/home/user/evasion_payload/target/release/evasion_payload"
    oracle_bin = "/usr/local/bin/oracle_wrapper.sh"

    assert os.path.exists(agent_bin), f"Agent binary not found at {agent_bin}"
    assert os.path.isfile(agent_bin), f"Agent path {agent_bin} is not a file"
    assert os.access(agent_bin, os.X_OK), f"Agent binary at {agent_bin} is not executable"

    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"
    assert os.access(oracle_bin, os.X_OK), f"Oracle binary at {oracle_bin} is not executable"

    random.seed(42)
    # Use ASCII printable characters for fuzzing
    printable_chars = string.printable

    for i in range(100):
        length = random.randint(1, 256)
        test_input = "".join(random.choice(printable_chars) for _ in range(length))

        # Run oracle
        try:
            oracle_res = subprocess.run(
                [oracle_bin, test_input],
                capture_output=True,
                text=False,
                check=True
            )
            oracle_out = oracle_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {repr(test_input)} with stderr: {e.stderr}")

        # Run agent
        try:
            agent_res = subprocess.run(
                [agent_bin, test_input],
                capture_output=True,
                text=False,
                check=True
            )
            agent_out = agent_res.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent binary failed on input {repr(test_input)} with stderr: {e.stderr}")

        assert agent_out == oracle_out, (
            f"Output mismatch on iteration {i}.\n"
            f"Input: {repr(test_input)}\n"
            f"Expected (Oracle): {oracle_out}\n"
            f"Got (Agent): {agent_out}"
        )