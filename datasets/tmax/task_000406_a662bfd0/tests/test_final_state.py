# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_word():
    length = random.randint(1, 20)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_line():
    choices = [
        lambda: ''.join(random.choices(string.printable, k=random.randint(0, 100))),
        lambda: f"FILE: {generate_random_word()}",
        lambda: f"  FILE: {generate_random_word()}  ",
        lambda: f"STATUS: {generate_random_word()}",
        lambda: f" STATUS: OK ",
        lambda: "STATUS: OK",
        lambda: f"ID: {random.randint(1, 10000)}",
        lambda: "",
        lambda: "   ",
    ]
    return random.choice(choices)()

def generate_input():
    num_lines = random.randint(5, 100)
    lines = [generate_random_line() for _ in range(num_lines)]
    return "\n".join(lines).encode('utf-8')

def test_script_exists_and_executable():
    script_path = "/home/user/parse_config.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."
    # We will test execution via bash so it doesn't strictly need +x, but let's check it anyway if possible.

def test_fuzz_equivalence():
    oracle_path = "/app/bin/tracker_parser"
    agent_script = "/home/user/parse_config.sh"

    assert os.path.exists(oracle_path), f"Oracle binary {oracle_path} missing."
    assert os.path.exists(agent_script), f"Agent script {agent_script} missing."

    random.seed(42)
    num_tests = 500

    for i in range(num_tests):
        test_input = generate_input()

        oracle_proc = subprocess.run(
            [oracle_path],
            input=test_input,
            capture_output=True
        )
        oracle_stdout = oracle_proc.stdout

        agent_proc = subprocess.run(
            ["/bin/bash", agent_script],
            input=test_input,
            capture_output=True
        )
        agent_stdout = agent_proc.stdout

        if oracle_stdout != agent_stdout:
            error_msg = (
                f"Mismatch on fuzz test {i+1}/{num_tests}.\n"
                f"Input:\n{test_input.decode('utf-8', errors='replace')}\n\n"
                f"Expected (Oracle) Output:\n{oracle_stdout.decode('utf-8', errors='replace')}\n\n"
                f"Actual (Agent) Output:\n{agent_stdout.decode('utf-8', errors='replace')}\n"
            )
            pytest.fail(error_msg)