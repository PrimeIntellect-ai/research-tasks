# test_final_state.py

import os
import json
import random
import string
import tempfile
import subprocess
import pytest

def test_xxhash_compiles():
    """Test that the xxHash vendored tool compiles successfully."""
    vendored_dir = "/app/vendored/xxHash-0.8.1"

    # Run make clean && make xxhsum
    clean_proc = subprocess.run(["make", "clean"], cwd=vendored_dir, capture_output=True)
    assert clean_proc.returncode == 0, f"make clean failed: {clean_proc.stderr.decode()}"

    make_proc = subprocess.run(["make", "xxhsum"], cwd=vendored_dir, capture_output=True)
    assert make_proc.returncode == 0, f"make xxhsum failed: {make_proc.stderr.decode()}"

    # Check that xxhsum can run
    xxhsum_path = os.path.join(vendored_dir, "xxhsum")
    assert os.path.isfile(xxhsum_path), "xxhsum binary not found after make"

    test_run = subprocess.run([xxhsum_path, "-H0"], input=b"test", capture_output=True)
    assert test_run.returncode == 0, f"xxhsum -H0 failed to run: {test_run.stderr.decode()}"

def generate_random_jsonl(num_lines):
    lines = []
    for _ in range(num_lines):
        record = {}
        # Randomly decide to include user_id
        if random.random() > 0.1:
            user_id_len = random.randint(1, 20)
            record["user_id"] = "".join(random.choices(string.ascii_letters + string.digits, k=user_id_len))

        # Randomly decide to include amount
        if random.random() > 0.1:
            amount = random.uniform(-500.0, 2000.0)
            # Sometimes format as string
            if random.random() > 0.8:
                record["amount"] = f"{amount:.4f}"
            else:
                record["amount"] = amount

        lines.append(json.dumps(record))
    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    """Test the agent's ETL script against the oracle on random inputs."""
    oracle_path = "/app/oracle_etl"
    agent_script = "/home/user/run_etl.sh"

    assert os.path.isfile(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script not found at {agent_script}"

    random.seed(42)

    for i in range(100):
        num_lines = random.randint(10, 1000)
        jsonl_data = generate_random_jsonl(num_lines)

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as tmp:
            tmp.write(jsonl_data)
            tmp_path = tmp.name

        try:
            # Run oracle
            oracle_proc = subprocess.run([oracle_path, tmp_path], capture_output=True, text=True)
            assert oracle_proc.returncode == 0, f"Oracle failed on input {i}: {oracle_proc.stderr}"
            oracle_out = oracle_proc.stdout

            # Run agent
            agent_proc = subprocess.run(["/bin/bash", agent_script, tmp_path], capture_output=True, text=True)
            assert agent_proc.returncode == 0, f"Agent script failed on input {i}: {agent_proc.stderr}"
            agent_out = agent_proc.stdout

            if oracle_out != agent_out:
                pytest.fail(f"Output mismatch on fuzz iteration {i}.\n\nInput (first 5 lines):\n" +
                            "\n".join(jsonl_data.splitlines()[:5]) +
                            f"\n\nExpected output (first 500 chars):\n{oracle_out[:500]}\n\n" +
                            f"Actual output (first 500 chars):\n{agent_out[:500]}")
        finally:
            os.remove(tmp_path)