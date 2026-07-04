# test_final_state.py

import os
import random
import subprocess
import json
import pytest

def test_gonum_syntax_error_fixed():
    """Ensure that the syntax error in /app/gonum/stat/stat.go has been fixed."""
    stat_go_path = "/app/gonum/stat/stat.go"
    assert os.path.isfile(stat_go_path), f"File {stat_go_path} is missing."

    with open(stat_go_path, "r") as f:
        content = f.read()

    assert "returnn" not in content, f"The syntax error 'returnn' is still present in {stat_go_path}."

def test_executable_exists():
    """Ensure the agent's executable exists and is executable."""
    agent_exec = "/home/user/process"
    assert os.path.isfile(agent_exec), f"Agent executable not found at {agent_exec}."
    assert os.access(agent_exec, os.X_OK), f"File at {agent_exec} is not executable."

def generate_fuzz_csv():
    """Generate a random CSV string according to the fuzz distribution."""
    num_rows = random.randint(10, 1000)
    lines = ["category,x,y,z"]
    categories = ["A", "B", "C", "D", "E", "F"]
    invalid_values = ["", "NaN", "text", "foo", "1.2.3"]

    for _ in range(num_rows):
        cat = random.choice(categories)
        row = [cat]
        for _ in range(3):
            if random.random() < 0.05:
                row.append(random.choice(invalid_values))
            else:
                row.append(f"{random.uniform(-100.0, 100.0):.6f}")
        lines.append(",".join(row))
    return "\n".join(lines)

def test_fuzz_equivalence():
    """Compare the agent's executable against the oracle on N random inputs."""
    oracle_exec = "/app/oracle_process"
    agent_exec = "/home/user/process"

    assert os.path.isfile(oracle_exec), f"Oracle executable not found at {oracle_exec}."
    assert os.path.isfile(agent_exec), f"Agent executable not found at {agent_exec}."

    random.seed(42)

    for i in range(100):
        csv_input = generate_fuzz_csv()

        oracle_proc = subprocess.run([oracle_exec], input=csv_input.encode('utf-8'), capture_output=True)
        agent_proc = subprocess.run([agent_exec], input=csv_input.encode('utf-8'), capture_output=True)

        assert oracle_proc.returncode == 0, f"Oracle failed on input {i}:\n{oracle_proc.stderr.decode()}"
        assert agent_proc.returncode == 0, f"Agent failed on input {i}:\n{agent_proc.stderr.decode()}"

        oracle_out = oracle_proc.stdout.decode('utf-8').strip()
        agent_out = agent_proc.stdout.decode('utf-8').strip()

        try:
            oracle_json = json.loads(oracle_out)
        except json.JSONDecodeError:
            pytest.fail(f"Oracle produced invalid JSON on input {i}:\n{oracle_out}")

        try:
            agent_json = json.loads(agent_out)
        except json.JSONDecodeError:
            pytest.fail(f"Agent produced invalid JSON on input {i}:\n{agent_out}")

        assert agent_json == oracle_json, (
            f"Mismatch on fuzz input {i}.\n"
            f"Input CSV head:\n{csv_input[:200]}...\n"
            f"Oracle output:\n{oracle_out}\n"
            f"Agent output:\n{agent_out}"
        )