# test_final_state.py

import os
import random
import string
import subprocess
import tempfile
import shutil
import pytest

AGENT_SCRIPT = "/home/user/dedup_archive.py"
ORACLE_BIN = "/app/oracle/dedup_oracle.bin"
OBJECTS_DIR = "/home/user/backup_repo/objects"

def generate_random_log(num_records):
    lines = []
    for _ in range(num_records):
        year = random.randint(2000, 2025)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        timestamp = f"[{year:04d}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}]"
        lines.append(timestamp)

        num_body_lines = random.randint(1, 20)
        for _ in range(num_body_lines):
            length = random.randint(10, 100)
            body_line = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
            lines.append(body_line)
    return "\n".join(lines) + "\n"

def test_agent_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_BIN), f"Oracle binary not found at {ORACLE_BIN}"

    os.makedirs(OBJECTS_DIR, exist_ok=True)

    random.seed(42)
    N = 50

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N):
            num_records = random.randint(10, 500)
            log_content = generate_random_log(num_records)

            input_file = os.path.join(tmpdir, f"input_{i}.log")
            with open(input_file, "w") as f:
                f.write(log_content)

            agent_target = os.path.join(tmpdir, f"agent_target_{i}")
            oracle_target = os.path.join(tmpdir, f"oracle_target_{i}")
            os.makedirs(agent_target, exist_ok=True)
            os.makedirs(oracle_target, exist_ok=True)

            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_BIN, input_file, oracle_target],
                capture_output=True, text=True
            )
            assert oracle_proc.returncode == 0, f"Oracle failed on input {i}:\n{oracle_proc.stderr}"

            # Run agent
            agent_proc = subprocess.run(
                ["python3", AGENT_SCRIPT, input_file, agent_target],
                capture_output=True, text=True
            )
            assert agent_proc.returncode == 0, f"Agent failed on input {i}:\n{agent_proc.stderr}"

            # Compare index.txt
            agent_index = os.path.join(agent_target, "index.txt")
            oracle_index = os.path.join(oracle_target, "index.txt")

            assert os.path.isfile(agent_index), f"Agent did not create index.txt for input {i}"
            assert os.path.isfile(oracle_index), f"Oracle did not create index.txt for input {i}"

            with open(agent_index, "r") as f:
                agent_index_content = f.read()
            with open(oracle_index, "r") as f:
                oracle_index_content = f.read()

            assert agent_index_content == oracle_index_content, f"index.txt mismatch on input {i}"

            # Compare hard links
            agent_files = sorted(os.listdir(agent_target))
            oracle_files = sorted(os.listdir(oracle_target))

            assert agent_files == oracle_files, f"Directory contents mismatch on input {i}"

            for fname in agent_files:
                if fname == "index.txt":
                    continue
                agent_file = os.path.join(agent_target, fname)
                oracle_file = os.path.join(oracle_target, fname)

                agent_stat = os.stat(agent_file)
                oracle_stat = os.stat(oracle_file)

                assert agent_stat.st_ino == oracle_stat.st_ino, f"Inode mismatch for {fname} on input {i}"