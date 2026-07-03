# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_fuzz_inputs(n=100, seed=42):
    random.seed(seed)
    inputs = []
    chars = string.ascii_letters + string.digits + '/' + '_' + '.'

    for _ in range(n):
        length = random.randint(20, 80) # leave room for extensions and insertions

        # Base generation
        path_chars = random.choices(chars, k=length)

        # Ensure it's an absolute path
        path_chars[0] = '/'

        path = "".join(path_chars)

        # Apply constraints
        if random.random() < 0.20:
            insert_pos = random.randint(1, len(path) - 1)
            path = path[:insert_pos] + "beta" + path[insert_pos:]

        if random.random() < 0.30:
            insert_pos = random.randint(1, len(path) - 1)
            path = path[:insert_pos] + "arm64" + path[insert_pos:]

        # Extension
        ext_choice = random.random()
        if ext_choice < 0.40:
            ext = ".rar"
        elif ext_choice < 0.70:
            ext = ".zip"
        else:
            ext = ".tar.gz"

        path = path + ext
        inputs.append(path)

    return "\n".join(inputs) + "\n"

def test_curator_script_exists():
    assert os.path.isfile('/home/user/curator.sh'), "The script /home/user/curator.sh does not exist."

def test_fuzz_equivalence():
    agent_script = '/home/user/curator.sh'
    oracle_script = '/app/oracle.sh'

    assert os.path.isfile(oracle_script), f"Oracle script missing at {oracle_script}"

    input_data = generate_fuzz_inputs(n=100, seed=1337)

    try:
        oracle_proc = subprocess.run(
            ['/bin/bash', oracle_script],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Oracle script failed to execute. stderr: {e.stderr}")

    try:
        agent_proc = subprocess.run(
            ['/bin/bash', agent_script],
            input=input_data,
            text=True,
            capture_output=True,
            check=True
        )
        agent_output = agent_proc.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Agent script failed to execute. stderr: {e.stderr}")

    if oracle_output != agent_output:
        # To avoid massive output, we can find the first differing line
        oracle_lines = oracle_output.splitlines()
        agent_lines = agent_output.splitlines()

        diff_idx = -1
        for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
            if o_line != a_line:
                diff_idx = i
                break

        if diff_idx != -1:
            pytest.fail(f"Output mismatch at line {diff_idx + 1}.\nExpected: {oracle_lines[diff_idx]}\nGot:      {agent_lines[diff_idx]}")
        elif len(oracle_lines) != len(agent_lines):
            pytest.fail(f"Output line count mismatch. Expected {len(oracle_lines)} lines, got {len(agent_lines)} lines.")
        else:
            pytest.fail("Outputs do not match exactly.")