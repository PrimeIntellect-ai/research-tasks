# test_final_state.py

import os
import json
import random
import string
import subprocess
import tempfile
import pytest

AGENT_SCRIPT = "/home/user/doc_backup.py"
ORACLE_BINARY = "/app/tests/doc_backup_oracle"

def generate_fuzz_dir(base_dir, seed):
    random.seed(seed)

    # Create directories
    dirs = [base_dir]
    num_dirs = random.randint(5, 20)
    for i in range(num_dirs):
        parent = random.choice(dirs)
        d = os.path.join(parent, f"dir_{i}")
        os.makedirs(d, exist_ok=True)
        dirs.append(d)

    # Create files
    files = []
    num_files = random.randint(10, 100)
    for i in range(num_files):
        d = random.choice(dirs)
        f = os.path.join(d, f"file_{i}.txt")
        size = random.randint(0, 1024)
        content = "".join(random.choices(string.ascii_letters + string.digits, k=size))
        with open(f, "w") as fp:
            fp.write(content)
        files.append(f)

    # Create symlinks
    num_links = random.randint(1, 20)
    for i in range(num_links):
        d = random.choice(dirs)
        link = os.path.join(d, f"link_{i}")
        if not os.path.exists(link):
            # 50% chance to link to a file, 50% to a directory (potentially creating loops)
            if random.random() < 0.5 and files:
                target = random.choice(files)
            else:
                target = random.choice(dirs)

            # Use relative paths for symlinks to make them interesting
            try:
                rel_target = os.path.relpath(target, d)
                os.symlink(rel_target, link)
            except Exception:
                pass

def test_agent_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing: {AGENT_SCRIPT}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_BINARY), f"Oracle missing: {ORACLE_BINARY}"

    N = 50
    for i in range(N):
        with tempfile.TemporaryDirectory() as base_dir:
            generate_fuzz_dir(base_dir, seed=42+i)

            agent_out = os.path.join(base_dir, "agent_manifest.json")
            oracle_out = os.path.join(base_dir, "oracle_manifest.json")

            # Run agent
            agent_cmd = ["python3", AGENT_SCRIPT, base_dir, agent_out]
            agent_proc = subprocess.run(agent_cmd, capture_output=True, text=True)
            assert agent_proc.returncode == 0, f"Agent script failed on seed {42+i}:\n{agent_proc.stderr}"

            # Run oracle
            oracle_cmd = [ORACLE_BINARY, base_dir, oracle_out]
            oracle_proc = subprocess.run(oracle_cmd, capture_output=True, text=True)
            assert oracle_proc.returncode == 0, f"Oracle failed on seed {42+i}:\n{oracle_proc.stderr}"

            # Compare outputs
            assert os.path.exists(agent_out), "Agent did not produce output file."
            assert os.path.exists(oracle_out), "Oracle did not produce output file."

            with open(agent_out, "r") as f:
                try:
                    agent_data = json.load(f)
                except json.JSONDecodeError:
                    pytest.fail("Agent output is not valid JSON.")

            with open(oracle_out, "r") as f:
                oracle_data = json.load(f)

            assert agent_data == oracle_data, f"Mismatch on seed {42+i}.\nOracle: {oracle_data}\nAgent: {agent_data}"

            # Check exact formatting (2-space indent, sorted keys)
            with open(agent_out, "r") as f:
                agent_raw = f.read()

            expected_raw = json.dumps(oracle_data, indent=2, sort_keys=True)
            assert agent_raw.strip() == expected_raw.strip(), f"Agent JSON formatting does not match exact requirements on seed {42+i}."