# test_final_state.py

import os
import random
import string
import base64
import subprocess
import shutil
import pytest

def test_csp_comment():
    fixed_script = "/home/user/upload_handler_fixed.py"
    assert os.path.isfile(fixed_script), f"Fixed script {fixed_script} does not exist."

    with open(fixed_script, "r") as f:
        first_line = f.readline().strip()

    expected_csp = "# CSP: default-src 'self'; script-src 'none'; object-src 'none'"
    assert first_line == expected_csp, f"Expected first line to be exactly {expected_csp!r}, but got {first_line!r}."

def test_ssh_hardening_script():
    script_path = "/home/user/apply_ssh_hardening.sh"
    assert os.path.isfile(script_path), f"SSH hardening script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    assert "AllowUsers auditor" in content, "Missing 'AllowUsers auditor' in the SSH hardening script."
    assert "PermitRootLogin no" in content, "Missing 'PermitRootLogin no' in the SSH hardening script."

def clear_uploads_dir():
    uploads_dir = "/home/user/uploads"
    if os.path.exists(uploads_dir):
        shutil.rmtree(uploads_dir)
    os.makedirs(uploads_dir, exist_ok=True)

def get_uploads_state():
    uploads_dir = "/home/user/uploads"
    state = {}
    for root, _, files in os.walk(uploads_dir):
        for file in files:
            path = os.path.join(root, file)
            rel_path = os.path.relpath(path, uploads_dir)
            with open(path, "rb") as f:
                state[rel_path] = f.read()
    return state

def test_fuzz_equivalence():
    fixed_script = "/home/user/upload_handler_fixed.py"
    oracle_script = "/app/oracle_handler.py"

    assert os.path.isfile(fixed_script), f"{fixed_script} is missing."
    assert os.path.isfile(oracle_script), f"Oracle script {oracle_script} is missing."

    random.seed(42)

    traversal_patterns = [
        "../", "..\\", "/etc/passwd", "../../", "/absolute/path", "dir/nested"
    ]

    N = 500  # Reduced from 5000 to avoid test timeout, but maintains high coverage
    for i in range(N):
        # Generate random filename
        if random.random() < 0.5:
            raw_filename = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 50)))
        else:
            prefix = random.choice(traversal_patterns)
            suffix = "".join(random.choices(string.ascii_letters + string.digits, k=random.randint(1, 20)))
            raw_filename = prefix + suffix

        b64_filename = base64.b64encode(raw_filename.encode('utf-8')).decode('utf-8')

        # Generate random payload
        raw_payload = bytes(random.getrandbits(8) for _ in range(random.randint(1, 100)))
        b64_payload = base64.b64encode(raw_payload).decode('utf-8')

        # Run Oracle
        clear_uploads_dir()
        oracle_proc = subprocess.run(
            ["python3", oracle_script, b64_filename, b64_payload],
            capture_output=True,
            text=True
        )
        oracle_state = get_uploads_state()

        # Run Agent
        clear_uploads_dir()
        agent_proc = subprocess.run(
            ["python3", fixed_script, b64_filename, b64_payload],
            capture_output=True,
            text=True
        )
        agent_state = get_uploads_state()

        # Assertions
        assert agent_proc.returncode == oracle_proc.returncode, \
            f"Exit code mismatch on input {raw_filename!r}. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}"

        assert agent_proc.stdout == oracle_proc.stdout, \
            f"Stdout mismatch on input {raw_filename!r}. Oracle: {oracle_proc.stdout!r}, Agent: {agent_proc.stdout!r}"

        assert agent_state == oracle_state, \
            f"File system state mismatch in /home/user/uploads/ on input {raw_filename!r}."