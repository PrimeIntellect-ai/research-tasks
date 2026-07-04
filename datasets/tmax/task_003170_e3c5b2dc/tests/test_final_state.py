# test_final_state.py
import os
import random
import subprocess
import pytest

ORACLE_PATH = "/app/oracle_exec"
AGENT_PATH = "/home/user/pipeline_exec"

def test_executable_exists():
    """Check if the agent executable exists and is executable."""
    assert os.path.isfile(AGENT_PATH), f"Executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"File at {AGENT_PATH} is not executable"

def generate_fuzz_input():
    n_limit = random.randint(1, 200)
    num_rows = random.randint(10, 5000)
    statuses = ["active", "inactive", "pending", "deleted"]

    lines = [str(n_limit)]
    for _ in range(num_rows):
        id_val = random.randint(1, 100000)
        status = random.choice(statuses)
        age = random.randint(18, 80)
        score = random.randint(0, 10000)
        lines.append(f"{id_val},{status},{age},{score}")

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    """Run fuzz equivalence testing between the oracle and the agent executable."""
    assert os.path.isfile(ORACLE_PATH), f"Oracle not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle at {ORACLE_PATH} is not executable"

    random.seed(42)
    num_tests = 50

    for i in range(num_tests):
        fuzz_input = generate_fuzz_input()

        oracle_proc = subprocess.run(
            [ORACLE_PATH],
            input=fuzz_input,
            text=True,
            capture_output=True,
            check=False
        )

        agent_proc = subprocess.run(
            [AGENT_PATH],
            input=fuzz_input,
            text=True,
            capture_output=True,
            check=False
        )

        # We don't strictly enforce return code matching if both succeed, but we do check output.
        oracle_out = oracle_proc.stdout.strip()
        agent_out = agent_proc.stdout.strip()

        if oracle_out != agent_out:
            input_preview = "\n".join(fuzz_input.splitlines()[:10])
            pytest.fail(
                f"Output mismatch on fuzz input {i + 1}.\n"
                f"Input preview (first 10 lines):\n{input_preview}\n...\n\n"
                f"Oracle Output (first 500 chars):\n{oracle_out[:500]}\n\n"
                f"Agent Output (first 500 chars):\n{agent_out[:500]}"
            )