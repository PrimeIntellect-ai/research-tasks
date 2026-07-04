# test_final_state.py

import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/semver_oracle"
AGENT_PATH = "/home/user/vparser_cpp/vparser"
NUM_TESTS = 1000

def generate_fuzz_inputs(seed=42):
    random.seed(seed)
    lines = []
    tags = ["dev", "alpha", "beta", "rc", "final", ""]
    malformed_tags = ["omega", "gamma", "unknown"]

    for _ in range(NUM_TESTS):
        num_versions = random.randint(2, 15)
        versions = []
        for _ in range(num_versions):
            is_malformed = random.random() < 0.1
            if is_malformed:
                malform_type = random.choice(["missing_minor", "invalid_tag", "not_a_version"])
                if malform_type == "missing_minor":
                    versions.append(f"{random.randint(0, 50)}")
                elif malform_type == "invalid_tag":
                    versions.append(f"{random.randint(0, 50)}.{random.randint(0, 50)}.{random.randint(0, 50)}-{random.choice(malformed_tags)}")
                else:
                    versions.append("just-some-random-string")
            else:
                major = random.randint(0, 50)
                minor = random.randint(0, 50)
                patch = random.randint(0, 50)
                tag = random.choice(tags)
                if tag:
                    versions.append(f"{major}.{minor}.{patch}-{tag}")
                else:
                    versions.append(f"{major}.{minor}.{patch}")
        lines.append(" ".join(versions))
    return "\n".join(lines) + "\n"

def test_agent_binary_exists():
    assert os.path.exists(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Expected file at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    input_data = generate_fuzz_inputs(seed=1337)

    # Run oracle
    oracle_proc = subprocess.run(
        [ORACLE_PATH],
        input=input_data,
        text=True,
        capture_output=True
    )

    # Run agent
    agent_proc = subprocess.run(
        [AGENT_PATH],
        input=input_data,
        text=True,
        capture_output=True
    )

    if oracle_proc.stdout != agent_proc.stdout:
        # Find the first mismatching line to provide a helpful error message
        oracle_lines = oracle_proc.stdout.splitlines()
        agent_lines = agent_proc.stdout.splitlines()

        for i, (o_line, a_line) in enumerate(zip(oracle_lines, agent_lines)):
            if o_line != a_line:
                pytest.fail(f"Stdout mismatch at output line {i+1}.\nOracle: {o_line!r}\nAgent:  {a_line!r}")

        if len(oracle_lines) != len(agent_lines):
            pytest.fail(f"Stdout line count mismatch. Oracle lines: {len(oracle_lines)}, Agent lines: {len(agent_lines)}")

        pytest.fail("Stdout mismatch (exact content differs).")

    if oracle_proc.stderr != agent_proc.stderr:
        pytest.fail(f"Stderr mismatch.\nOracle stderr: {oracle_proc.stderr!r}\nAgent stderr: {agent_proc.stderr!r}")