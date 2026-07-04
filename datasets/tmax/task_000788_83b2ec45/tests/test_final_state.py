# test_final_state.py

import os
import subprocess
import tempfile
import random
import string
import hashlib
import shutil

import pytest

AGENT_SCRIPT = "/home/user/secure_checker.sh"
ORACLE_SCRIPT = "/app/oracle_checker"
POLICY_FILE = "/home/user/policy.txt"

def test_policy_file_exists():
    assert os.path.isfile(POLICY_FILE), f"Decrypted policy file missing at {POLICY_FILE}"

def test_agent_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script missing at {AGENT_SCRIPT}"
    assert os.access(AGENT_SCRIPT, os.X_OK), f"Agent script at {AGENT_SCRIPT} is not executable"

def generate_random_filename(malicious=False):
    length = random.randint(5, 15)
    if not malicious:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

    # Malicious filename
    base = "".join(random.choices(string.ascii_letters + string.digits, k=length//2))
    evil_chars = [" ", "'", "\"", ";", "$", "(", ")", "\n", "`", "&", "|", "<", ">", "\\", "*", "?", "-"]
    evil_part = "".join(random.choices(evil_chars, k=random.randint(1, 3)))
    suffix = "".join(random.choices(string.ascii_letters + string.digits, k=length//2))
    return f"{base}{evil_part}{suffix}"

def get_policy_hashes():
    if not os.path.isfile(POLICY_FILE):
        return []
    with open(POLICY_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def test_fuzz_equivalence():
    random.seed(42)

    # We will try to create files that match policy hashes sometimes
    policy_hashes = get_policy_hashes()

    # For matching hashes, we need the actual content. Since we only have the hashes, 
    # we can't easily generate matching content unless we know it. 
    # However, the task says "Some files will have contents matching hashes...". 
    # If we can't generate matching content, we just generate random bytes. 
    # The agent script and oracle script will both just output [FAIL] for them, which is fine for equivalence.

    for i in range(50):
        with tempfile.TemporaryDirectory() as tmpdir:
            num_files = random.randint(1, 20)
            for _ in range(num_files):
                is_malicious = random.random() < 0.4
                fname = generate_random_filename(malicious=is_malicious)

                # Ensure unique filename
                while os.path.exists(os.path.join(tmpdir, fname)):
                    fname = generate_random_filename(malicious=is_malicious)

                fpath = os.path.join(tmpdir, fname)

                # Write random bytes
                size = random.randint(0, 1024)
                content = os.urandom(size)

                with open(fpath, "wb") as f:
                    f.write(content)

            # Run agent
            agent_proc = subprocess.run(
                [AGENT_SCRIPT, tmpdir],
                capture_output=True,
                text=True
            )

            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_SCRIPT, tmpdir],
                capture_output=True,
                text=True
            )

            assert agent_proc.returncode == oracle_proc.returncode, \
                f"Return code mismatch on iteration {i}. Agent: {agent_proc.returncode}, Oracle: {oracle_proc.returncode}"

            assert agent_proc.stdout == oracle_proc.stdout, \
                f"Stdout mismatch on iteration {i} for directory {tmpdir}.\nAgent stdout:\n{agent_proc.stdout}\nOracle stdout:\n{oracle_proc.stdout}"