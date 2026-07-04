# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_fuzz_inputs(n=5000, seed=42):
    random.seed(seed)
    lines = []

    alphanumeric = string.ascii_letters + string.digits

    for _ in range(n):
        choice = random.random()
        if choice < 0.70:
            # Valid line
            id_len = random.randint(1, 15)
            id_str = ''.join(random.choice(alphanumeric) for _ in range(id_len))
            ts = random.randint(0, 100000)
            data_len = random.randint(1, 50)
            data_str = ''.join(random.choice(alphanumeric) for _ in range(data_len))
            lines.append(f"ID:{id_str}|TS:{ts}|DATA:{data_str}")
        elif choice < 0.80:
            # Comment line
            comment_len = random.randint(1, 20)
            comment_str = ''.join(random.choice(alphanumeric) for _ in range(comment_len))
            lines.append(f"#{comment_str}")
        elif choice < 0.90:
            # Empty line
            lines.append("")
        else:
            # Malformed line
            malform_type = random.choice([1, 2, 3])
            if malform_type == 1:
                lines.append("ID:only_id_no_pipes")
            elif malform_type == 2:
                lines.append("ID:abc|TS:abc|DATA:abc") # TS is not int, wait, oracle just matches format? The prompt says "random integer timestamps". Let's just break the format.
            else:
                lines.append("random_garbage_without_tags")

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    agent_script = "/home/user/log_parser.py"
    oracle_bin = "/app/oracle_parser"
    offset = "37"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_bin), f"Oracle binary not found at {oracle_bin}"

    input_data = generate_fuzz_inputs(n=5000, seed=1337)

    # Run oracle
    oracle_cmd = [oracle_bin, offset]
    oracle_proc = subprocess.run(
        oracle_cmd,
        input=input_data,
        text=True,
        capture_output=True
    )
    assert oracle_proc.returncode == 0, f"Oracle failed to run: {oracle_proc.stderr}"

    # Run agent
    agent_cmd = ["python3", agent_script, offset]
    agent_proc = subprocess.run(
        agent_cmd,
        input=input_data,
        text=True,
        capture_output=True
    )

    if agent_proc.returncode != 0:
        pytest.fail(f"Agent script crashed or returned non-zero exit code.\nStderr: {agent_proc.stderr}")

    oracle_output = oracle_proc.stdout.splitlines()
    agent_output = agent_proc.stdout.splitlines()

    input_lines = input_data.splitlines()

    # We compare line by line to give better error messages if possible, 
    # but since empty/comment lines produce no output, the output length is shorter than input length.
    # We'll just compare the entire output lists.
    if oracle_output != agent_output:
        # Find the first difference
        min_len = min(len(oracle_output), len(agent_output))
        for i in range(min_len):
            if oracle_output[i] != agent_output[i]:
                pytest.fail(f"Output mismatch at output line {i+1}.\nExpected (Oracle): {oracle_output[i]}\nGot (Agent): {agent_output[i]}")

        # If one is longer than the other
        pytest.fail(f"Output length mismatch. Oracle produced {len(oracle_output)} lines, Agent produced {len(agent_output)} lines.")