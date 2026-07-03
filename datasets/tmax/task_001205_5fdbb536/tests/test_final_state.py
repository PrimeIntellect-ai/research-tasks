# test_final_state.py
import os
import subprocess
import random
import pytest

def test_fuzz_equivalence():
    """
    Test that the agent's parser matches the oracle parser byte-for-byte
    on 1000 random 20-character hex strings.
    """
    oracle_path = "/app/oracle_parser"
    agent_path = "/home/user/parser.py"

    assert os.path.exists(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent script not found at {agent_path}"

    random.seed(42)
    hex_chars = "0123456789abcdef"

    num_tests = 1000

    for i in range(num_tests):
        # Generate 20 random hex characters (10 bytes)
        test_input = "".join(random.choices(hex_chars, k=20))

        # Run oracle
        oracle_cmd = [oracle_path, test_input]
        oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True)

        # Run agent
        agent_cmd = ["python3", agent_path, test_input]
        agent_res = subprocess.run(agent_cmd, capture_output=True, text=True)

        # Assert return codes are 0 (or at least match, but usually 0 for valid hex)
        assert agent_res.returncode == oracle_res.returncode, \
            f"Return code mismatch on input {test_input}: oracle={oracle_res.returncode}, agent={agent_res.returncode}\nAgent stderr: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, \
            f"Output mismatch on input {test_input}!\nOracle output: {oracle_out}\nAgent output: {agent_out}"