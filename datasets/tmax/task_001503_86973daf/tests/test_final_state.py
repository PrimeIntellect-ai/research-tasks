# test_final_state.py

import os
import subprocess
import random
import string
import pytest

def test_part1_secret_key():
    """Verify that the secret key was correctly extracted from the video."""
    secret_file = "/home/user/secret_key.txt"
    assert os.path.isfile(secret_file), f"File {secret_file} does not exist."

    with open(secret_file, "r") as f:
        content = f.read().strip()

    expected_secret = "SUPER_SECRET_TRAFFIC_KEY_9921"
    assert content == expected_secret, f"Expected secret key '{expected_secret}', but found '{content}'"

def generate_fuzz_inputs(n=10000, seed=42):
    random.seed(seed)
    inputs = []
    tokens = [
        "[TLS:OK]", "<script>", "javascript:", "' OR ", "UNION SELECT", "root ", "admin "
    ]
    chars = string.ascii_letters + string.digits + string.punctuation + " "

    for _ in range(n):
        length = random.randint(10, 150)
        base_str = "".join(random.choice(chars) for _ in range(length))

        # Randomly insert targeted tokens
        if random.random() < 0.5:
            token = random.choice(tokens)
            insert_pos = random.randint(0, len(base_str))
            base_str = base_str[:insert_pos] + token + base_str[insert_pos:]

        # Sometimes prepend root/admin to test username logic
        if random.random() < 0.2:
            token = random.choice(["root ", "admin "])
            base_str = token + base_str

        inputs.append(base_str)

    return inputs

def test_part2_log_analyzer_fuzz_equivalence():
    """Fuzz the agent's log analyzer against the oracle binary."""
    project_dir = "/home/user/log_analyzer"
    assert os.path.isdir(project_dir), f"Rust project directory {project_dir} does not exist."

    # Compile the agent's project
    build_cmd = ["cargo", "build", "--release"]
    build_result = subprocess.run(build_cmd, cwd=project_dir, capture_output=True, text=True)
    assert build_result.returncode == 0, f"Failed to compile agent's Rust project:\n{build_result.stderr}"

    agent_binary = os.path.join(project_dir, "target/release/log_analyzer")
    assert os.path.isfile(agent_binary), f"Agent binary not found at {agent_binary}"

    oracle_binary = "/app/oracle_log_analyzer"
    assert os.path.isfile(oracle_binary), f"Oracle binary not found at {oracle_binary}"

    inputs = generate_fuzz_inputs(n=10000)
    input_data = "\n".join(inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        [oracle_binary],
        input=input_data,
        capture_output=True,
        text=True
    )
    assert oracle_proc.returncode == 0, "Oracle failed to execute."
    oracle_output = oracle_proc.stdout.splitlines()

    # Run agent
    agent_proc = subprocess.run(
        [agent_binary],
        input=input_data,
        capture_output=True,
        text=True
    )
    assert agent_proc.returncode == 0, f"Agent binary failed to execute:\n{agent_proc.stderr}"
    agent_output = agent_proc.stdout.splitlines()

    assert len(oracle_output) == len(inputs), "Oracle output length mismatch."
    assert len(agent_output) == len(inputs), f"Agent output length mismatch. Expected {len(inputs)}, got {len(agent_output)}"

    for i, (inp, expected, actual) in enumerate(zip(inputs, oracle_output, agent_output)):
        assert expected == actual, (
            f"Mismatch on input {i}:\n"
            f"Input: {inp!r}\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )