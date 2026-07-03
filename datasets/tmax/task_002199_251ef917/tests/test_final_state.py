# test_final_state.py

import os
import random
import subprocess
import pytest

def test_fixed_format_script_exists_and_executable():
    script_path = "/app/fixed_format.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_fuzz_equivalence():
    oracle_path = "/opt/verifier/oracle_processor"
    agent_script = "/app/fixed_format.sh"

    assert os.path.isfile(oracle_path), f"Oracle program {oracle_path} is missing."

    # Fixed seed for reproducibility
    random.seed(42)

    # Generate 1000 random byte strings
    # lengths 1 to 255
    # including spaces, ASCII control characters, shell metacharacters, invalid UTF-8

    # Interesting bytes to include frequently
    interesting_bytes = (
        list(range(0, 32)) + # Control characters
        [ord(c) for c in " *?<>|&;\"'\n\t\r\\$()[]{}"] + # Shell metacharacters and spaces
        [255, 254, 128, 129] # Invalid UTF-8 bytes
    )
    all_bytes = list(range(256))

    num_iterations = 1000

    for i in range(num_iterations):
        length = random.randint(1, 255)
        # Mix interesting bytes and random bytes
        input_bytes = bytearray()
        for _ in range(length):
            if random.random() < 0.3:
                input_bytes.append(random.choice(interesting_bytes))
            else:
                input_bytes.append(random.choice(all_bytes))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path, input_bytes],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Run agent
        agent_proc = subprocess.run(
            ["/bin/bash", agent_script, input_bytes],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Exit code mismatch on iteration {i}.\n"
            f"Input (repr): {input_bytes!r}\n"
            f"Oracle exit code: {oracle_proc.returncode}\n"
            f"Agent exit code: {agent_proc.returncode}\n"
            f"Agent stderr: {agent_proc.stderr!r}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on iteration {i}.\n"
            f"Input (repr): {input_bytes!r}\n"
            f"Oracle stdout: {oracle_proc.stdout!r}\n"
            f"Agent stdout: {agent_proc.stdout!r}\n"
            f"Agent stderr: {agent_proc.stderr!r}"
        )