# test_final_state.py
import os
import random
import subprocess
import pytest

def test_api_parser_fuzz_equivalence():
    agent_script = "/home/user/api_parser.py"
    oracle_bin = "/app/oracle_parser"

    assert os.path.isfile(agent_script), f"{agent_script} does not exist."
    assert os.path.isfile(oracle_bin), f"{oracle_bin} does not exist."

    random.seed(42)
    for _ in range(100):
        length = random.randint(16, 128)
        binary_string = "".join(random.choice("01") for _ in range(length))

        oracle_cmd = [oracle_bin, binary_string]
        agent_cmd = ["/usr/bin/python3", agent_script, binary_string]

        try:
            oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True)
            oracle_output = oracle_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on input {binary_string}: {e.stderr}")

        try:
            agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, check=True)
            agent_output = agent_res.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on input {binary_string}: {e.stderr}")

        assert oracle_output == agent_output, (
            f"Mismatch on input {binary_string}.\n"
            f"Oracle output: {oracle_output}\n"
            f"Agent output: {agent_output}"
        )

def test_integration_result():
    result_file = "/home/user/integration_result.txt"
    assert os.path.isfile(result_file), f"{result_file} does not exist."
    with open(result_file, "r") as f:
        content = f.read().strip()

    expected_result = "4219"
    assert content == expected_result, f"Expected integration result '{expected_result}', got '{content}'"