# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import pytest

AGENT_PATH = "/home/user/analyzer"
ORACLE_PATH = "/opt/oracle/analyzer_oracle"
ITERATIONS = 50

@pytest.fixture(scope="session")
def check_executables():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent file at {AGENT_PATH} is not executable"

    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle file at {ORACLE_PATH} is not executable"

def generate_random_csv(filepath: str, seed: int):
    rng = random.Random(seed)
    num_rows = rng.randint(100, 1000)

    with open(filepath, 'w') as f:
        for _ in range(num_rows):
            col1 = rng.randint(0, 99)
            col2 = rng.choice(string.ascii_uppercase)
            col3 = round(rng.uniform(0.0, 100.0), 4)
            f.write(f"{col1},{col2},{col3}\n")

def test_fuzz_equivalence(check_executables):
    for i in range(ITERATIONS):
        seed = 42 + i
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            csv_path = tmp.name

        try:
            generate_random_csv(csv_path, seed)

            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_PATH, csv_path],
                capture_output=True,
                text=True
            )
            assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i} (seed {seed})"

            # Run agent
            agent_proc = subprocess.run(
                [AGENT_PATH, csv_path],
                capture_output=True,
                text=True
            )
            assert agent_proc.returncode == 0, f"Agent failed on iteration {i} (seed {seed})"

            oracle_out = oracle_proc.stdout.strip()
            agent_out = agent_proc.stdout.strip()

            if oracle_out != agent_out:
                # Truncate output for failure message if too long
                oracle_show = oracle_out[:500] + ("..." if len(oracle_out) > 500 else "")
                agent_show = agent_out[:500] + ("..." if len(agent_out) > 500 else "")

                with open(csv_path, 'r') as f:
                    csv_content = f.read()
                csv_show = csv_content[:500] + ("..." if len(csv_content) > 500 else "")

                pytest.fail(
                    f"Mismatch on iteration {i} (seed {seed}).\n\n"
                    f"Input CSV snippet:\n{csv_show}\n\n"
                    f"Oracle Output snippet:\n{oracle_show}\n\n"
                    f"Agent Output snippet:\n{agent_show}\n"
                )
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)