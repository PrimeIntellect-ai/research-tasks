# test_final_state.py
import os
import random
import subprocess
import string
import pytest

def generate_random_path(existing_paths, action):
    if action == "DELETE" and existing_paths:
        return random.choice(list(existing_paths))
    elif action == "MODIFY" and existing_paths:
        return random.choice(list(existing_paths))
    else:
        # CREATE or fallback if no existing paths
        depth = random.randint(1, 4)
        parts = []
        for _ in range(depth):
            name_len = random.randint(3, 8)
            name = ''.join(random.choices(string.ascii_letters + string.digits, k=name_len))
            parts.append(name)
        # Add a file extension sometimes
        if random.choice([True, False]):
            parts[-1] += ".txt"
        return "/" + "/".join(parts)

def generate_fuzz_input(num_lines):
    lines = []
    existing_paths = set()
    timestamp = 1
    for _ in range(num_lines):
        if not existing_paths:
            action = "CREATE"
        else:
            action = random.choices(["CREATE", "MODIFY", "DELETE"], weights=[50, 30, 20])[0]

        path = generate_random_path(existing_paths, action)

        if action == "CREATE":
            existing_paths.add(path)
            size = random.randint(1, 10000)
        elif action == "MODIFY":
            size = random.randint(1, 10000)
        elif action == "DELETE":
            existing_paths.remove(path)
            size = 0

        lines.append(f"[{timestamp}] {action} {path} {size}")
        timestamp += random.randint(1, 5)

    return "\n".join(lines) + "\n"

def test_extracted_oracle_exists_and_executable():
    path = "/home/user/oracle_tracker"
    assert os.path.isfile(path), f"Extracted oracle not found at {path}"
    assert os.access(path, os.X_OK), f"Extracted oracle at {path} is not executable"

def test_agent_executable_exists():
    path = "/home/user/doc_tracker"
    assert os.path.isfile(path), f"Agent executable not found at {path}"
    assert os.access(path, os.X_OK), f"Agent executable at {path} is not executable"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_tracker_hidden"
    agent_path = "/home/user/doc_tracker"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent executable missing at {agent_path}"

    random.seed(42)
    N = 500

    for i in range(N):
        num_lines = random.randint(10, 200)
        input_data = generate_fuzz_input(num_lines)

        try:
            oracle_proc = subprocess.run(
                [oracle_path],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=2
            )
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail("Oracle timed out.")

        try:
            agent_proc = subprocess.run(
                [agent_path],
                input=input_data,
                text=True,
                capture_output=True,
                timeout=2
            )
            agent_out = agent_proc.stdout.strip()
        except subprocess.TimeoutExpired:
            pytest.fail("Agent executable timed out on fuzz input.")

        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Return code mismatch on input:\n{input_data}\nExpected: {oracle_proc.returncode}, Got: {agent_proc.returncode}"

        assert agent_out == oracle_out, \
            f"Output mismatch on input:\n{input_data}\nExpected:\n{oracle_out}\nGot:\n{agent_out}"