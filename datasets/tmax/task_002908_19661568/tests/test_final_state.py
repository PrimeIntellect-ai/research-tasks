# test_final_state.py

import os
import stat
import random
import subprocess
import pytest

def test_routing_rules_permissions():
    path = "/home/user/routing_rules"
    assert os.path.isdir(path), f"Directory {path} does not exist."
    st = os.stat(path)
    mode = stat.S_IMODE(st.st_mode)
    assert mode == 0o700, f"Expected permissions 0700 for {path}, but got {oct(mode)}"

def test_startup_script_exports():
    path = "/home/user/startup.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "TZ=UTC" in content, "startup.sh does not seem to export TZ=UTC"
    assert "LC_ALL=C" in content, "startup.sh does not seem to export LC_ALL=C"

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_filter"
    agent_path = "/home/user/router_migrator/target/release/router_migrator"

    assert os.path.isfile(oracle_path), f"Oracle program missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent program missing at {agent_path}"

    random.seed(42)
    inputs = []
    for _ in range(10000):
        ip = f"10.{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        inputs.append(ip)

    input_str = "\n".join(inputs) + "\n"
    input_bytes = input_str.encode("utf-8")

    env = os.environ.copy()
    env["TZ"] = "UTC"
    env["LC_ALL"] = "C"

    oracle_proc = subprocess.run(
        [oracle_path],
        input=input_bytes,
        capture_output=True,
        env=env
    )
    assert oracle_proc.returncode == 0, "Oracle program failed to execute."
    oracle_out = oracle_proc.stdout.decode("utf-8")

    agent_proc = subprocess.run(
        [agent_path],
        input=input_bytes,
        capture_output=True,
        env=env
    )
    assert agent_proc.returncode == 0, "Agent program failed to execute."
    agent_out = agent_proc.stdout.decode("utf-8")

    oracle_lines = oracle_out.splitlines()
    agent_lines = agent_out.splitlines()

    assert len(oracle_lines) == len(agent_lines), "Output line counts differ between oracle and agent."

    for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
        if o_line != a_line:
            pytest.fail(
                f"Mismatch at input line {i+1} (IP: {inputs[i]}).\n"
                f"Oracle output: {o_line}\n"
                f"Agent output:  {a_line}"
            )