# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_fuzz_input(seed):
    random.seed(seed)
    num_lines = random.randint(1, 50)
    lines = []

    # Avoid newlines and carriage returns in the base character set 
    # to maintain the expected number of lines.
    chars = string.ascii_letters + string.digits + string.punctuation + ' \t'

    for _ in range(num_lines):
        length = random.randint(10, 500)
        line = "".join(random.choices(chars, k=length))

        # 20% chance to include a random 16-digit sequence
        if random.random() < 0.20:
            digits = "".join(random.choices(string.digits, k=16))
            insert_pos = random.randint(0, len(line))
            # Pad with spaces to ensure it is bounded by non-digits
            line = line[:insert_pos] + " " + digits + " " + line[insert_pos:]

        # 10% chance to include a 15-digit or 17-digit sequence
        if random.random() < 0.10:
            k = random.choice([15, 17])
            digits = "".join(random.choices(string.digits, k=k))
            insert_pos = random.randint(0, len(line))
            line = line[:insert_pos] + " " + digits + " " + line[insert_pos:]

        # 20% chance to include "Hummingbird"
        if random.random() < 0.20:
            insert_pos = random.randint(0, len(line))
            line = line[:insert_pos] + "Hummingbird" + line[insert_pos:]

        # 20% chance to include "' OR 1=1 --"
        if random.random() < 0.20:
            insert_pos = random.randint(0, len(line))
            line = line[:insert_pos] + "' OR 1=1 --" + line[insert_pos:]

        lines.append(line)

    # Join with newlines, and randomly decide if the very last line has a trailing newline
    result = "\n".join(lines)
    if random.random() < 0.5:
        result += "\n"

    return result

def test_fuzz_equivalence():
    agent_script = "/home/user/redactor.py"
    oracle_script = "/app/oracle_redactor"

    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"
    assert os.path.exists(oracle_script), f"Oracle script not found at {oracle_script}"

    # Run 1000 fuzz tests
    for i in range(1000):
        input_data = generate_fuzz_input(i)

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_script],
            input=input_data,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input seed {i}:\n{oracle_proc.stderr}"

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script],
            input=input_data,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, (
            f"Agent script failed or crashed on input seed {i}.\n"
            f"Error output:\n{agent_proc.stderr}"
        )

        if oracle_proc.stdout != agent_proc.stdout:
            pytest.fail(
                f"Output mismatch on input seed {i}.\n\n"
                f"--- Input ---\n{input_data!r}\n\n"
                f"--- Expected Output (Oracle) ---\n{oracle_proc.stdout!r}\n\n"
                f"--- Actual Output (Agent) ---\n{agent_proc.stdout!r}"
            )