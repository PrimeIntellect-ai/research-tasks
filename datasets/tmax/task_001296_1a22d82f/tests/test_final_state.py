# test_final_state.py
import os
import random
import string
import subprocess
import pytest

ORACLE_PATH = "/app/legacy_processor"
AGENT_SCRIPT = "/home/user/pipeline.py"

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_valid_line():
    id_val = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(3, 5)))
    x_val = f"{random.uniform(0.0, 100.0):.2f}"
    y_val = f"{random.uniform(0.0, 100.0):.2f}"

    parts = [
        f"ID={id_val}",
        f"X={x_val}",
        f"Y={y_val}",
        generate_random_string(random.randint(5, 15)),
        generate_random_string(random.randint(5, 15))
    ]
    random.shuffle(parts)
    return " ".join(parts) + "\n"

def generate_noise_line():
    return generate_random_string(random.randint(20, 60)) + "\n"

def generate_input_stream():
    num_lines = random.randint(100, 500)
    lines = []
    for _ in range(num_lines):
        if random.random() < 0.7:
            lines.append(generate_valid_line())
        else:
            lines.append(generate_noise_line())
    return "".join(lines)

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"

    random.seed(42)

    for i in range(100):
        input_data = generate_input_stream()

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=input_data,
            text=True,
            capture_output=True,
            check=False
        )
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["python3", AGENT_SCRIPT],
            input=input_data,
            text=True,
            capture_output=True,
            check=False
        )
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on iteration {i}.\n\n"
                f"--- Input preview (first 300 chars) ---\n{input_data[:300]}\n...\n\n"
                f"--- Oracle output preview ---\n{oracle_out[:300]}\n...\n\n"
                f"--- Agent output preview ---\n{agent_out[:300]}\n..."
            )