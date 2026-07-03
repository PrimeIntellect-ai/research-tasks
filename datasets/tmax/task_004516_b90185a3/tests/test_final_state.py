# test_final_state.py

import os
import subprocess
import tempfile
import random
import string
import json

def generate_wal_file(path, num_lines):
    operations = ["INSERT", "UPDATE", "DELETE"]
    with open(path, "w") as f:
        for _ in range(num_lines):
            ts = random.uniform(1600000000.0, 1700000000.0)
            op = random.choice(operations)
            key = f"key_{random.randint(1, 100)}"
            val = ''.join(random.choices(string.ascii_letters, k=8))
            # Write a generic JSON-like or space-separated log line
            # Since we don't know the exact format, we provide a generic one
            # that might be parsed or at least processed by the tool.
            line = json.dumps({"timestamp": ts, "operation": op, "key": key, "value": val})
            f.write(f"{line}\n")

def test_fuzz_equivalence():
    oracle_path = "/app/oracle_processor"
    agent_path = "/home/user/fixed_processor.py"

    assert os.path.isfile(agent_path), f"Agent program {agent_path} does not exist."
    assert os.access(oracle_path, os.X_OK), f"Oracle program {oracle_path} is not executable."

    random.seed(42)

    for i in range(5): # 5 fuzz iterations
        with tempfile.TemporaryDirectory() as tmpdir:
            num_files = random.randint(10, 20)
            for j in range(num_files):
                file_path = os.path.join(tmpdir, f"wal_{j}.log")
                num_lines = random.randint(100, 500)
                generate_wal_file(file_path, num_lines)

            # Run oracle
            oracle_cmd = [oracle_path, tmpdir]
            oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)

            # Run agent
            agent_cmd = ["python3", agent_path, tmpdir]
            agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)

            assert oracle_proc.returncode == agent_proc.returncode, \
                f"Return code mismatch on fuzz dir {i}: oracle={oracle_proc.returncode}, agent={agent_proc.returncode}"

            assert oracle_proc.stdout == agent_proc.stdout, \
                f"Stdout mismatch on fuzz dir {i}.\nOracle:\n{oracle_proc.stdout[:500]}\n\nAgent:\n{agent_proc.stdout[:500]}"