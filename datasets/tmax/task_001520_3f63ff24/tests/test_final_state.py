# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_fuzz_equivalence():
    agent_script = "/home/user/solution.py"
    oracle_bin = "/app/oracle_bin"

    assert os.path.exists(agent_script), f"Agent script {agent_script} does not exist."
    assert os.path.exists(oracle_bin), f"Oracle binary {oracle_bin} does not exist."

    # Generate 1000 random alphanumeric strings, length 10-50
    random.seed(42)
    num_tests = 1000
    inputs = []
    for _ in range(num_tests):
        length = random.randint(10, 50)
        s = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        inputs.append(s)

    input_data = '\n'.join(inputs) + '\n'

    # Run oracle
    try:
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle binary failed unexpectedly:\n{e.stderr}")

    # Run agent script
    agent_proc = subprocess.run(
        ["python3", agent_script],
        input=input_data,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent script failed with error:\n{agent_proc.stderr}"

    agent_output = agent_proc.stdout

    if oracle_output != agent_output:
        oracle_lines = oracle_output.splitlines()
        agent_lines = agent_output.splitlines()

        # Find the first mismatch to provide a helpful error message
        for i, in_str in enumerate(inputs):
            o_line = oracle_lines[i] if i < len(oracle_lines) else "<missing>"
            a_line = agent_lines[i] if i < len(agent_lines) else "<missing>"

            if o_line != a_line:
                pytest.fail(
                    f"Mismatch on input '{in_str}' (line {i+1}).\n"
                    f"Oracle output: '{o_line}'\n"
                    f"Agent output:  '{a_line}'"
                )

        # Fallback if the loop didn't catch it (e.g. trailing newlines)
        assert len(oracle_lines) == len(agent_lines), f"Output line counts differ: Oracle={len(oracle_lines)}, Agent={len(agent_lines)}"
        assert oracle_output == agent_output, "Outputs differ in whitespace or formatting."