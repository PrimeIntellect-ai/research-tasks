# test_final_state.py
import os
import subprocess
import random
import string
import json
import gzip
import tempfile
import pytest

ORACLE_PATH = "/opt/oracle/process_archive_oracle.sh"
AGENT_PATH = "/home/user/process_archive.sh"
UNARCHIVE_SCRIPT = "/app/log-archiver-1.0/bin/unarchive.sh"

def generate_archive(filepath):
    """Generate a valid custom backup archive file."""
    metadata_len = random.randint(20, 200)
    # Create dummy JSON metadata of roughly metadata_len length
    key_len = max(1, metadata_len - 20)
    metadata = json.dumps({"meta": "".join(random.choices(string.ascii_letters, k=key_len))})
    metadata_bytes = metadata.encode('utf-8')

    num_logs = random.randint(1, 100)
    severities = ["INFO", "WARN", "ERROR", "DEBUG"]
    log_data = ""
    for _ in range(num_logs):
        sev = random.choice(severities)
        msg_len = random.randint(10, 500)
        # Avoid creating new log headers inside the message
        msg_chars = random.choices(string.ascii_letters + " \n.,!?", k=msg_len)
        msg = "".join(msg_chars).replace("[20", "x20") 
        # Generate a random timestamp
        year = random.randint(2020, 2023)
        month = f"{random.randint(1, 12):02d}"
        day = f"{random.randint(1, 28):02d}"
        hour = f"{random.randint(0, 23):02d}"
        minute = f"{random.randint(0, 59):02d}"
        second = f"{random.randint(0, 59):02d}"
        log_data += f"[{year}-{month}-{day} {hour}:{minute}:{second}] [{sev}] {msg}\n"

    gzipped_log = gzip.compress(log_data.encode('utf-8'))

    with open(filepath, 'wb') as f:
        header_hex = f"{len(metadata_bytes):08X}".encode('ascii')
        f.write(header_hex + b"\n")
        f.write(metadata_bytes)
        f.write(gzipped_log)

def test_unarchive_bug_fixed():
    """Verify that the unarchive.sh script was fixed."""
    assert os.path.exists(UNARCHIVE_SCRIPT), f"{UNARCHIVE_SCRIPT} is missing."
    with open(UNARCHIVE_SCRIPT, "r") as f:
        content = f.read()

    # The bug was `$GZ_BIN -d -c "$1"` without GZ_BIN defined.
    # A valid fix either defines GZ_BIN or replaces it with `gzip`.
    # To be robust, we just ensure it's executable and we'll see if it works in the fuzz test.
    assert os.access(UNARCHIVE_SCRIPT, os.X_OK), f"{UNARCHIVE_SCRIPT} must be executable."

def test_fuzz_equivalence():
    """Fuzz test the agent's script against the oracle."""
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script {AGENT_PATH} is not executable. Run chmod +x."

    random.seed(1337)
    severities = ["INFO", "WARN", "ERROR", "DEBUG"]

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(500):
            archive_path = os.path.join(tmpdir, f"archive_{i}.bin")
            generate_archive(archive_path)
            target_sev = random.choice(severities)

            oracle_proc = subprocess.run([ORACLE_PATH, archive_path, target_sev], capture_output=True)
            agent_proc = subprocess.run([AGENT_PATH, archive_path, target_sev], capture_output=True)

            if agent_proc.returncode != oracle_proc.returncode:
                pytest.fail(f"Return code mismatch on input {i} (Severity: {target_sev}).\n"
                            f"Oracle exited with {oracle_proc.returncode}, Agent exited with {agent_proc.returncode}.\n"
                            f"Agent stderr: {agent_proc.stderr.decode(errors='replace')}")

            if agent_proc.stdout != oracle_proc.stdout:
                pytest.fail(f"Output mismatch on input {i} (Severity: {target_sev}).\n"
                            f"Expected {len(oracle_proc.stdout)} bytes, got {len(agent_proc.stdout)} bytes.\n"
                            f"Agent stderr: {agent_proc.stderr.decode(errors='replace')}")