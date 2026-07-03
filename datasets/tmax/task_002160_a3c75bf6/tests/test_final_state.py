# test_final_state.py

import os
import sys
import random
import subprocess
import pytest

def test_pysm_lib_installed():
    """Verify that pysm-lib was successfully installed into the system Python environment."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "show", "pysm-lib"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, "pysm-lib is not installed. Did you run pip install successfully?"
    assert "Name: pysm-lib" in result.stdout, "pysm-lib package details not found in pip show output."

def generate_fuzz_inputs(n=5000):
    """Generate N random inputs for the fuzz equivalence test."""
    random.seed(42)
    inputs = []
    for _ in range(n):
        lines = []
        num_lines = random.randint(0, 100)
        for _ in range(num_lines):
            choice = random.random()
            if choice < 0.6:
                cmd = random.choice(["INIT", "ADD", "MUL"])
                val = random.randint(-1000, 1000)
                line = f"{cmd} {val}"
            elif choice < 0.8:
                line = "EMIT"
            else:
                line = random.choice([
                    "INVALID_CMD", 
                    "INIT", 
                    "ADD", 
                    "MUL", 
                    "INIT 10 20", 
                    "ADD abc", 
                    "MUL 10 20",
                    "EMIT extra",
                    ""
                ])

            # Apply random whitespace padding
            if random.random() < 0.25:
                line = " \t " + line + "  "
            lines.append(line)
        inputs.append("\n".join(lines) + "\n")
    return inputs

def test_fuzz_equivalence():
    """Verify bit-exact equivalence between the oracle and the agent's new parser."""
    oracle_path = "/app/oracle/legacy_parser"
    agent_path = "/home/user/new_parser.py"

    assert os.path.isfile(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}"

    inputs = generate_fuzz_inputs(5000)

    for i, inp in enumerate(inputs):
        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path], 
            input=inp, 
            text=True, 
            capture_output=True
        )

        # Run agent
        agent_proc = subprocess.run(
            [sys.executable, agent_path], 
            input=inp, 
            text=True, 
            capture_output=True
        )

        # We only care about stdout matching exactly as per instructions
        if oracle_proc.stdout != agent_proc.stdout:
            error_msg = (
                f"Mismatch on fuzz input #{i}!\n\n"
                f"--- INPUT ---\n{inp}\n"
                f"--- ORACLE STDOUT ---\n{oracle_proc.stdout}\n"
                f"--- AGENT STDOUT ---\n{agent_proc.stdout}\n"
            )
            pytest.fail(error_msg)