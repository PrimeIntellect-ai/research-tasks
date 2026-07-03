# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def generate_fuzz_input(seed):
    random.seed(seed)
    lines_count = random.randint(0, 500)
    lines = []
    chars = string.ascii_letters + string.digits
    for _ in range(lines_count):
        if random.random() < 0.7:
            # Generate valid semver
            semver = f"{random.randint(0, 100)}.{random.randint(0, 100)}.{random.randint(0, 100)}"
        else:
            # Generate invalid semver
            choices = [
                f"{random.randint(0, 100)}.{random.randint(0, 100)}",
                "invalid",
                f"{random.randint(0, 100)}.{random.randint(0, 100)}.{random.randint(0, 100)}.{random.randint(0, 100)}",
                "a.b.c"
            ]
            semver = random.choice(choices)

        text_len = random.randint(1, 100)
        text = "".join(random.choices(chars, k=text_len))
        lines.append(f"{semver} {text}")

    return "\n".join(lines) + ("\n" if lines else "")

def test_fuzz_equivalence():
    oracle_path = "/app/oracle"
    agent_path = "/home/user/bin/log-processor"

    assert os.path.exists(agent_path), f"Agent binary missing at {agent_path}"
    assert os.path.isfile(agent_path), f"Agent path {agent_path} is not a file"
    assert os.access(agent_path, os.X_OK), f"Agent binary at {agent_path} is not executable"

    for i in range(1000):
        input_data = generate_fuzz_input(i)

        oracle_proc = subprocess.run([oracle_path], input=input_data, text=True, capture_output=True)
        agent_proc = subprocess.run([agent_path], input=input_data, text=True, capture_output=True)

        assert agent_proc.returncode == oracle_proc.returncode, (
            f"Return code mismatch on input seed {i}.\n"
            f"Oracle return code: {oracle_proc.returncode}\n"
            f"Agent return code: {agent_proc.returncode}\n"
            f"Input data:\n{input_data}"
        )

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Stdout mismatch on input seed {i}.\n"
            f"Input data:\n{input_data}\n"
            f"Oracle stdout:\n{oracle_proc.stdout}\n"
            f"Agent stdout:\n{agent_proc.stdout}"
        )

def test_ci_workflow_exists():
    ci_path = "/home/user/repo/.github/workflows/ci.yml"
    assert os.path.exists(ci_path), f"CI workflow file missing at {ci_path}"
    assert os.path.isfile(ci_path), f"CI path {ci_path} is not a file"

    with open(ci_path, "r") as f:
        content = f.read()

    assert "cargo build" in content, "CI workflow missing 'cargo build'"
    assert "cargo test" in content, "CI workflow missing 'cargo test'"