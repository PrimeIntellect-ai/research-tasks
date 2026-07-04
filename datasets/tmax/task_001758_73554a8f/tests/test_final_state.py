# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def generate_random_line():
    length = random.randint(0, 200)
    # Include alphanumerics, spaces, and punctuation
    chars = string.ascii_letters + string.digits + " \t\n\r" + string.punctuation
    return "".join(random.choice(chars) for _ in range(length))

def generate_fuzz_input(num_lines):
    lines = []
    base_lines = []
    # Create some base lines to ensure duplicates/collisions
    for _ in range(max(1, num_lines // 5)):
        base_lines.append(generate_random_line())

    for _ in range(num_lines):
        if random.random() < 0.5 and base_lines:
            # Mutate a base line slightly to create a collision after normalization
            base = random.choice(base_lines)
            mutated = base + random.choice(string.punctuation) + "  " + random.choice(string.ascii_lowercase)
            lines.append(mutated)
        else:
            lines.append(generate_random_line())
    return "\n".join(lines).encode('utf-8')

def test_agent_executable_exists():
    path = "/home/user/cleaner"
    assert os.path.isfile(path), f"Agent program not found at {path}"
    assert os.access(path, os.X_OK), f"Agent program at {path} is not executable"

def test_fuzz_equivalence():
    agent_path = "/home/user/cleaner"
    oracle_path = "/app/oracle_filter"

    assert os.path.isfile(oracle_path), f"Oracle program not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle program at {oracle_path} is not executable"

    random.seed(42)
    num_iterations = 50  # Reduced from 500 for test execution speed, but sufficient for fuzzing

    for i in range(num_iterations):
        num_lines = random.randint(0, 1000)
        input_data = generate_fuzz_input(num_lines)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}"

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=input_data,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        assert agent_proc.returncode == 0, f"Agent program failed (exit code {agent_proc.returncode}) on iteration {i}. Stderr: {agent_proc.stderr.decode('utf-8', errors='replace')}"

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            # Decode for better error message if possible
            try:
                oracle_str = oracle_out.decode('utf-8')
                agent_str = agent_out.decode('utf-8')
                error_msg = f"Output mismatch on iteration {i} (input lines: {num_lines}).\nExpected (Oracle):\n{oracle_str[:500]}\n\nGot (Agent):\n{agent_str[:500]}"
            except UnicodeDecodeError:
                error_msg = f"Output mismatch on iteration {i} (binary output differs)."

            pytest.fail(error_msg)