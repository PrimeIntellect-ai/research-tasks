# test_final_state.py

import os
import time
import random
import subprocess
from pathlib import Path

def test_scripts_exist():
    """Check if the required Bash scripts have been created."""
    archive_script = Path("/home/user/custom_archive.sh")
    extract_script = Path("/home/user/custom_extract.sh")

    assert archive_script.is_file(), f"Script {archive_script} does not exist."
    assert extract_script.is_file(), f"Script {extract_script} does not exist."

def test_log_files_renamed():
    """Check if files older than 7 days are renamed to .archive_pending."""
    logs_dir = Path("/app/logs_incoming")
    assert logs_dir.is_dir(), f"Directory {logs_dir} does not exist."

    current_time = time.time()
    seven_days_in_seconds = 7 * 24 * 60 * 60

    # We check all files in the directory.
    # Note: Since the user renamed them, we check the current files.
    for f in logs_dir.iterdir():
        if f.is_file():
            mtime = f.stat().st_mtime
            age = current_time - mtime
            is_older_than_7_days = age > seven_days_in_seconds
            has_extension = f.name.endswith(".archive_pending")

            if is_older_than_7_days:
                assert has_extension, f"File {f.name} is older than 7 days but does not have .archive_pending extension."
            else:
                assert not has_extension, f"File {f.name} is newer than 7 days but has .archive_pending extension."

def test_fuzz_archive_equivalence():
    """Fuzz test custom_archive.sh against archive_oracle."""
    random.seed(42)
    oracle_path = "/app/bin/archive_oracle"
    agent_cmd = ["bash", "/home/user/custom_archive.sh"]

    assert os.path.isfile(oracle_path), f"Oracle {oracle_path} not found."

    for i in range(100):
        length = random.randint(10, 10000)
        # Increase probability of null bytes to properly test the RLE logic
        input_data = bytearray(random.choices(b'\x00\x00\x00' + bytes(range(256)), k=length))

        oracle_proc = subprocess.run([oracle_path], input=input_data, capture_output=True)
        agent_proc = subprocess.run(agent_cmd, input=input_data, capture_output=True)

        assert oracle_proc.returncode == 0, "Oracle failed on compression."
        assert agent_proc.returncode == 0, "Agent script failed on compression."

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Mismatch in compression output on iteration {i}. "
            f"Input length: {length}. "
            f"Oracle output length: {len(oracle_proc.stdout)}, "
            f"Agent output length: {len(agent_proc.stdout)}."
        )

def test_fuzz_extract_equivalence():
    """Fuzz test custom_extract.sh against extract_oracle."""
    random.seed(1337)
    archive_oracle_path = "/app/bin/archive_oracle"
    extract_oracle_path = "/app/bin/extract_oracle"
    agent_cmd = ["bash", "/home/user/custom_extract.sh"]

    assert os.path.isfile(extract_oracle_path), f"Oracle {extract_oracle_path} not found."

    for i in range(100):
        length = random.randint(10, 10000)
        raw_data = bytearray(random.choices(b'\x00\x00\x00' + bytes(range(256)), k=length))

        # First compress with oracle to get valid compressed input
        compress_proc = subprocess.run([archive_oracle_path], input=raw_data, capture_output=True)
        assert compress_proc.returncode == 0, "Oracle failed on compression."
        compressed_data = compress_proc.stdout

        oracle_proc = subprocess.run([extract_oracle_path], input=compressed_data, capture_output=True)
        agent_proc = subprocess.run(agent_cmd, input=compressed_data, capture_output=True)

        assert oracle_proc.returncode == 0, "Oracle failed on extraction."
        assert agent_proc.returncode == 0, "Agent script failed on extraction."

        assert agent_proc.stdout == oracle_proc.stdout, (
            f"Mismatch in extraction output on iteration {i}. "
            f"Compressed input length: {len(compressed_data)}. "
            f"Oracle output length: {len(oracle_proc.stdout)}, "
            f"Agent output length: {len(agent_proc.stdout)}."
        )