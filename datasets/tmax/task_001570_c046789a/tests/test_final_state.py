# test_final_state.py

import os
import random
import subprocess
import pytest

AGENT_EXE = "/home/user/pk_solver/target/release/pk_solver"
ORACLE_EXE = "/app/oracle_pk_solver"
NUM_RUNS = 10

def test_agent_executable_exists():
    """Verify that the agent's executable exists and is executable."""
    assert os.path.isfile(AGENT_EXE), f"Agent executable not found at {AGENT_EXE}. Did you compile in release mode?"
    assert os.access(AGENT_EXE, os.X_OK), f"Agent executable at {AGENT_EXE} is not executable."

def test_fuzz_equivalence():
    """Fuzz the agent's implementation against the oracle."""
    assert os.path.isfile(ORACLE_EXE), f"Oracle executable not found at {ORACLE_EXE}"

    random.seed(42)

    for run_idx in range(NUM_RUNS):
        num_lines = random.randint(1, 1000)
        inputs = [str(random.randint(0, 20000)) for _ in range(num_lines)]
        input_str = "\n".join(inputs) + "\n"

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_EXE],
            input=input_str,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_out = oracle_proc.stdout

        # Run agent
        try:
            agent_proc = subprocess.run(
                [AGENT_EXE],
                input=input_str,
                text=True,
                capture_output=True,
                timeout=30  # Generous timeout for up to 1000 lines of 20000 iterations
            )
        except subprocess.TimeoutExpired:
            pytest.fail(f"Agent executable timed out on fuzzing run {run_idx}. Make sure your implementation is efficient.")

        assert agent_proc.returncode == 0, (
            f"Agent executable failed with return code {agent_proc.returncode} on run {run_idx}.\n"
            f"Stderr: {agent_proc.stderr}"
        )

        agent_out = agent_proc.stdout

        if oracle_out != agent_out:
            oracle_lines = oracle_out.splitlines()
            agent_lines = agent_out.splitlines()

            for i, (ol, al) in enumerate(zip(oracle_lines, agent_lines)):
                if ol != al:
                    pytest.fail(
                        f"Output mismatch on fuzzing run {run_idx}, for input N={inputs[i]}.\n"
                        f"Expected (Oracle): {ol}\n"
                        f"Actual (Agent):    {al}"
                    )

            # If zip finished but lengths differ
            assert len(oracle_lines) == len(agent_lines), (
                f"Output length mismatch on fuzzing run {run_idx}.\n"
                f"Expected {len(oracle_lines)} lines, got {len(agent_lines)} lines."
            )