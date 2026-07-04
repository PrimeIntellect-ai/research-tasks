# test_final_state.py
import os
import subprocess
import random
import string
import pytest

N_ITERATIONS = 500

def generate_log_line():
    year = random.randint(2000, 2025)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    level = random.choice(["INFO", "WARN", "ERROR", "DEBUG", "TRACE"])

    chars = string.ascii_letters + string.digits + " _:.-"
    payload_len = random.randint(5, 50)
    payload = "".join(random.choice(chars) for _ in range(payload_len))

    return f"{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d} [{level}] {payload}"

def generate_input():
    num_lines = random.randint(1, 50)
    return "\n".join(generate_log_line() for _ in range(num_lines)) + "\n"

def test_locking_fixed():
    lock_file_path = '/app/vendored_logparser/vendored_logparser/locking.py'
    assert os.path.exists(lock_file_path), "locking.py is missing"

    with open(lock_file_path, 'r') as f:
        content = f.read()

    # Check that fcntl is actually imported and not just commented out
    lines = content.splitlines()
    has_active_import = any(line.strip() == 'import fcntl' for line in lines)
    assert has_active_import, "The `import fcntl` statement is still commented out or missing in locking.py"

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/log_transformer_oracle"
    agent_path = "/home/user/log_transformer.py"

    assert os.path.exists(agent_path), f"Agent script not found at {agent_path}"
    assert os.path.exists(oracle_path), f"Oracle script not found at {oracle_path}"

    # Ensure the vendored package is in PYTHONPATH so both scripts can import it
    env = os.environ.copy()
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"/app/vendored_logparser:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = "/app/vendored_logparser"

    random.seed(42)

    for i in range(N_ITERATIONS):
        test_input = generate_input()

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=test_input,
            text=True,
            capture_output=True,
            env=env
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}:\n{oracle_proc.stderr}"

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_path],
            input=test_input,
            text=True,
            capture_output=True,
            env=env
        )

        assert agent_proc.returncode == 0, f"Agent script failed on iteration {i}. Stderr:\n{agent_proc.stderr}"

        oracle_out = oracle_proc.stdout
        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            pytest.fail(
                f"Mismatch on iteration {i}.\n"
                f"Input:\n{test_input}\n"
                f"Expected (Oracle):\n{oracle_out}\n"
                f"Got (Agent):\n{agent_out}"
            )