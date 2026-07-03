# test_final_state.py
import os
import subprocess
import random
import pytest

AGENT_EXECUTABLE = "/home/user/etl_cleaner"
ORACLE_EXECUTABLE = "/app/oracle"
OUTPUT_FILE = "/home/user/cleaned_video_data.txt"
FUZZ_N = 50

def generate_fuzz_input():
    num_lines = random.randint(10, 500)
    lines = []
    types = ['I', 'P', 'B', 'i', 'p', 'b', 'IDR']
    for _ in range(num_lines):
        timestamp = random.uniform(0.0, 100.0)
        size = random.randint(100, 10000)
        typ = random.choice(types)
        retry_id = random.randint(1, 5)
        lines.append(f"{timestamp:.4f},{size},{typ},{retry_id}")
    return "\n".join(lines) + "\n"

def test_agent_executable_exists():
    assert os.path.exists(AGENT_EXECUTABLE), f"Agent executable {AGENT_EXECUTABLE} not found."
    assert os.access(AGENT_EXECUTABLE, os.X_OK), f"Agent executable {AGENT_EXECUTABLE} is not executable."

def test_output_file_exists():
    assert os.path.exists(OUTPUT_FILE), f"Output file {OUTPUT_FILE} not found."
    assert os.path.getsize(OUTPUT_FILE) > 0, f"Output file {OUTPUT_FILE} is empty."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_EXECUTABLE), f"Oracle executable {ORACLE_EXECUTABLE} not found."

    random.seed(42)

    for i in range(FUZZ_N):
        input_data = generate_fuzz_input()

        try:
            agent_proc = subprocess.run(
                [AGENT_EXECUTABLE],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=5
            )
            agent_out = agent_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent program failed on fuzz iteration {i}.\nInput:\n{input_data}\nStderr:\n{e.stderr}")
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent program timed out on fuzz iteration {i}.")

        try:
            oracle_proc = subprocess.run(
                [ORACLE_EXECUTABLE],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
                timeout=5
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle program failed on fuzz iteration {i}.\nInput:\n{input_data}\nStderr:\n{e.stderr}")

        if agent_out != oracle_out:
            pytest.fail(
                f"Mismatch on fuzz iteration {i}.\n"
                f"Input (first 5 lines):\n{chr(10).join(input_data.splitlines()[:5])}\n...\n"
                f"Expected Output:\n{oracle_out}\n"
                f"Agent Output:\n{agent_out}\n"
            )