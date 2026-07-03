# test_final_state.py

import os
import subprocess
import random
import pytest

AGENT_EXECUTABLE = "/home/user/etl_fix"
ORACLE_EXECUTABLE = "/app/ref_process"
N_TESTS = 1000

def generate_random_csv(seed):
    random.seed(seed)
    num_lines = random.randint(0, 500)

    lines = ["time,s1,s2,s3"]
    last_line = None

    for _ in range(num_lines):
        if last_line is not None and random.random() < 0.15:
            lines.append(last_line)
            continue

        t = random.randint(0, 5000)

        row = [str(t)]
        for _ in range(3):
            if random.random() < 0.20:
                row.append("-1")
            else:
                row.append(str(random.randint(0, 1000)))

        line = ",".join(row)
        lines.append(line)
        last_line = line

    return "\n".join(lines) + "\n"

def test_executable_exists():
    assert os.path.isfile(AGENT_EXECUTABLE), f"Agent executable not found at {AGENT_EXECUTABLE}"
    assert os.access(AGENT_EXECUTABLE, os.X_OK), f"Agent executable at {AGENT_EXECUTABLE} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_EXECUTABLE), f"Oracle executable not found at {ORACLE_EXECUTABLE}"

    for i in range(N_TESTS):
        csv_input = generate_random_csv(seed=i)

        try:
            oracle_proc = subprocess.run(
                [ORACLE_EXECUTABLE],
                input=csv_input,
                text=True,
                capture_output=True,
                check=True
            )
            oracle_out = oracle_proc.stdout
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on seed {i}. Stderr: {e.stderr}")

        try:
            agent_proc = subprocess.run(
                [AGENT_EXECUTABLE],
                input=csv_input,
                text=True,
                capture_output=True,
                check=True,
                timeout=2
            )
            agent_out = agent_proc.stdout
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent executable timed out on seed {i}. Input:\n{csv_input}")
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent executable failed on seed {i}. Stderr: {e.stderr}\nInput:\n{csv_input}")

        if oracle_out != agent_out:
            pytest.fail(
                f"Output mismatch on seed {i}.\n\n"
                f"Input:\n{csv_input}\n"
                f"Expected Output (Oracle):\n{oracle_out}\n"
                f"Actual Output (Agent):\n{agent_out}"
            )