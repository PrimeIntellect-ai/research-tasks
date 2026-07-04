# test_final_state.py
import os
import random
import string
import subprocess
import pytest

AGENT_SCRIPT = '/home/user/process_logs.py'
ORACLE_SCRIPT = '/app/oracle_process_logs.py'

def generate_fuzz_lines(n=1000, seed=42):
    random.seed(seed)
    lines = []

    jobs = ['JOB' + str(i) for i in range(10)]
    data_pool = [
        "Some random data",
        "  Leading and trailing   ",
        "Multiple    spaces   here",
        "ALL CAPS DATA",
        "mixed Case Data",
        "duplicate   data",
        "DUPLICATE DATA "
    ]

    for _ in range(n):
        choice = random.random()
        if choice < 0.2:
            # Completely random string
            length = random.randint(5, 50)
            rand_str = ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=length))
            lines.append(rand_str)
        elif choice < 0.8:
            # Valid log line
            ts = f"2023-10-01T{random.randint(10,23)}:{random.randint(10,59)}:{random.randint(10,59)}"
            job = random.choice(jobs)
            data = random.choice(data_pool)
            # maybe add some random whitespace
            if random.random() < 0.5:
                data += " " * random.randint(1, 5)
            lines.append(f"[{ts}] {job}: {data}")
        else:
            # Slightly malformed but close
            job = random.choice(jobs)
            data = random.choice(data_pool)
            lines.append(f"[{job}] : {data}")

    return "\n".join(lines) + "\n"

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} does not exist."
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script {AGENT_SCRIPT} is not executable."

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_SCRIPT), f"Oracle script {ORACLE_SCRIPT} is missing."

    input_data = generate_fuzz_lines(1000, seed=1337)

    # Run oracle
    oracle_proc = subprocess.run(
        [ORACLE_SCRIPT],
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )
    oracle_out = oracle_proc.stdout

    # Run agent
    agent_proc = subprocess.run(
        [AGENT_SCRIPT],
        input=input_data,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent script failed with error:\n{agent_proc.stderr}"

    agent_out = agent_proc.stdout

    if agent_out != oracle_out:
        # Find the first differing line for a helpful error message
        oracle_lines = oracle_out.splitlines()
        agent_lines = agent_out.splitlines()

        diff_msg = "Outputs differ.\n"
        for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
            if o_line != a_line:
                diff_msg += f"Mismatch at output line {i+1}:\nOracle: {o_line!r}\nAgent:  {a_line!r}\n"
                break

        if len(oracle_lines) != len(agent_lines):
            diff_msg += f"\nLine counts differ: Oracle has {len(oracle_lines)}, Agent has {len(agent_lines)}."

        pytest.fail(diff_msg)