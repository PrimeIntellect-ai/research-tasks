# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_random_word(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_fuzz_input(n=5000, seed=42):
    random.seed(seed)
    lines = []
    for _ in range(n):
        # Generate random alphanumeric words to form a line of 20-200 chars
        target_length = random.randint(20, 200)
        words = []
        current_length = 0
        while current_length < target_length:
            word = generate_random_word(random.randint(3, 10))
            words.append(word)
            current_length += len(word) + 1

        line = ' '.join(words)[:target_length]

        # 30% probabilities for each specific pattern
        if random.random() < 0.3:
            line += f" --password {generate_random_word(8)}"
        if random.random() < 0.3:
            line += f" Cookie: {generate_random_word(12)}"
        if random.random() < 0.3:
            line += f" Authorization: Bearer {generate_random_word(16)}"
        if random.random() < 0.3:
            line += " 8443"
        if random.random() < 0.3:
            line += " telemetry.internal.corp"

        # Shuffle the components of the line to mix patterns and random words
        line_parts = line.split()
        random.shuffle(line_parts)

        # Re-assemble preserving the exact patterns (since shuffle breaks multi-word patterns)
        # Actually, it's safer to just append or insert them at random positions to avoid breaking "Authorization: Bearer"

        # Let's rebuild the line generation to be safer
        parts = []
        while sum(len(p) for p in parts) + len(parts) < target_length:
            parts.append(generate_random_word(random.randint(3, 10)))

        if random.random() < 0.3:
            parts.append(f"--password {generate_random_word(8)}")
        if random.random() < 0.3:
            parts.append(f"Cookie: {generate_random_word(12)}")
        if random.random() < 0.3:
            parts.append(f"Authorization: Bearer {generate_random_word(16)}")
        if random.random() < 0.3:
            parts.append("8443")
        if random.random() < 0.3:
            parts.append("telemetry.internal.corp")

        random.shuffle(parts)
        lines.append(' '.join(parts) + '\n')

    return ''.join(lines)

def test_redactor_exists():
    assert os.path.isfile("/home/user/redactor.py"), "/home/user/redactor.py is missing"

def test_fuzz_equivalence():
    agent_script = "/home/user/redactor.py"
    oracle_script = "/app/oracle.py"

    assert os.path.isfile(agent_script), f"{agent_script} does not exist."
    assert os.path.isfile(oracle_script), f"{oracle_script} does not exist."

    input_data = generate_fuzz_input(n=5000, seed=1337)

    # Run oracle
    oracle_proc = subprocess.run(
        ["python3", oracle_script],
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )
    oracle_output = oracle_proc.stdout

    # Run agent
    agent_proc = subprocess.run(
        ["python3", agent_script],
        input=input_data,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent script failed with error:\n{agent_proc.stderr}"
    agent_output = agent_proc.stdout

    # Compare outputs line by line to provide a clear error message
    oracle_lines = oracle_output.splitlines(keepends=True)
    agent_lines = agent_output.splitlines(keepends=True)

    # Check if lengths match first to give a broad hint
    if len(oracle_lines) != len(agent_lines):
        # We will still find the first mismatch below, or report length difference
        pass

    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        assert o_line == a_line, (
            f"Mismatch at output line {i+1}.\n"
            f"Expected (Oracle): {repr(o_line)}\n"
            f"Got (Agent):       {repr(a_line)}\n"
        )

    assert len(oracle_lines) == len(agent_lines), (
        f"Output line count mismatch. Oracle produced {len(oracle_lines)} lines, "
        f"Agent produced {len(agent_lines)} lines."
    )