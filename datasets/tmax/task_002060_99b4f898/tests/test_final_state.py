# test_final_state.py

import os
import stat
import subprocess
import random
import string
import sys
import pytest

def test_run_ci_script():
    path = "/home/user/run_ci.sh"
    assert os.path.isfile(path), f"File {path} does not exist."

    # Check if executable
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

    with open(path, "r") as f:
        content = f.read()

    assert "/app/proxy-resolver/resolver.py" in content or "resolver.py" in content, \
        f"{path} does not seem to call the resolver.py script."

def test_resolver_cron():
    path = "/home/user/resolver.cron"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check for basic cron syntax for every 5 minutes
    assert "*/5 * * * *" in content, f"{path} does not contain the correct cron schedule (*/5 * * * *)."
    assert "/home/user/run_ci.sh" in content, f"{path} does not contain the command to run run_ci.sh."

def test_fuzz_equivalence():
    oracle_path = "/opt/oracle/resolver_oracle.py"
    agent_path = "/app/proxy-resolver/resolver.py"

    assert os.path.isfile(oracle_path), f"Oracle script missing at {oracle_path}."
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}."

    # Check if agent script is executable
    st = os.stat(agent_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {agent_path} is not executable."

    random.seed(42)

    def generate_ip():
        return ".".join(str(random.randint(0, 255)) for _ in range(4))

    def generate_domain():
        name = "".join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
        tld = random.choice(["com", "net", "org", "io"])
        return f"{name}.{tld}"

    inputs = []
    for _ in range(1000):
        inputs.append(f"{generate_ip()} {generate_domain()}")

    input_data = "\n".join(inputs) + "\n"

    # Run oracle
    oracle_proc = subprocess.run(
        [sys.executable, oracle_path],
        input=input_data,
        text=True,
        capture_output=True,
        check=True
    )
    oracle_output = oracle_proc.stdout.strip().split("\n")

    # Run agent
    agent_proc = subprocess.run(
        [sys.executable, agent_path],
        input=input_data,
        text=True,
        capture_output=True
    )

    assert agent_proc.returncode == 0, f"Agent script failed with error: {agent_proc.stderr}"

    agent_output = agent_proc.stdout.strip().split("\n")

    assert len(oracle_output) == len(inputs), "Oracle output length mismatch."
    assert len(agent_output) == len(inputs), f"Agent output length mismatch. Expected {len(inputs)}, got {len(agent_output)}."

    for i, (inp, oracle_res, agent_res) in enumerate(zip(inputs, oracle_output, agent_output)):
        assert oracle_res == agent_res, \
            f"Mismatch on input '{inp}'. Oracle produced '{oracle_res}', but agent produced '{agent_res}'."