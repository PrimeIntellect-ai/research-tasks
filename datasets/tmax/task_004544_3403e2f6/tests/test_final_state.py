# test_final_state.py
import os
import subprocess
import random
import string
import pytest

def generate_fuzz_input():
    """
    Generates a random input string matching the specified fuzz distribution:
    Randomized alphanumeric strings interleaved with random combinations of '../', './', 
    encoded path traversal characters (%2e%2e%2f), and HTML tags.
    Lengths between 10 and 500 characters.
    """
    target_length = random.randint(10, 500)

    malicious_components = [
        "../", "./", "%2e%2e%2f", 
        "<script>", "<img>", "<a>", 
        "onerror=alert(1)", "javascript:", "onload=eval()",
        "../../etc/passwd", "\"><script>alert(1)</script>"
    ]

    alphanumeric = string.ascii_letters + string.digits

    parts = []
    current_length = 0

    while current_length < target_length:
        if random.random() < 0.4:
            comp = random.choice(malicious_components)
            parts.append(comp)
            current_length += len(comp)
        else:
            chunk_len = random.randint(1, 15)
            comp = "".join(random.choices(alphanumeric, k=chunk_len))
            parts.append(comp)
            current_length += len(comp)

    return "".join(parts)[:target_length]

def test_sanitizer_fuzz_equivalence():
    """
    Tests the agent's sanitizer against the reference oracle using fuzzing.
    Ensures bit-exact equivalence on N random inputs.
    """
    agent_script = "/home/user/sanitizer.py"
    oracle_script = "/app/reference_sanitizer.py"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing: {oracle_script}"

    # Use a fixed seed for reproducibility
    random.seed(42)
    N = 1000  # Testing 1000 iterations to balance thoroughness and execution time

    for i in range(N):
        fuzz_input = generate_fuzz_input()

        # Run agent program
        agent_proc = subprocess.run(
            ["python3", agent_script, fuzz_input],
            capture_output=True,
            text=True
        )

        # Run oracle program
        oracle_proc = subprocess.run(
            ["python3", oracle_script, fuzz_input],
            capture_output=True,
            text=True
        )

        # Assert equivalence
        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on input: {repr(fuzz_input)}\n"
            f"Oracle returned {oracle_proc.returncode}, Agent returned {agent_proc.returncode}\n"
            f"Agent stderr: {agent_proc.stderr}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Output mismatch on input: {repr(fuzz_input)}\n"
            f"Expected (Oracle): {repr(oracle_proc.stdout)}\n"
            f"Got (Agent): {repr(agent_proc.stdout)}"
        )