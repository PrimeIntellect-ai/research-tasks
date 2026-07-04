# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_directory_created():
    expected_dir = "/home/user/loop_archive_8891f"
    assert os.path.isdir(expected_dir), f"The expected directory '{expected_dir}' was not created. Did you correctly extract the path from the video?"

def generate_random_hex(length):
    return ''.join(random.choices(string.hexdigits.lower(), k=length))

def generate_random_path():
    length = random.randint(4, 8)
    name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
    return f"/test/{name}"

def generate_manifest():
    num_lines = random.randint(10, 500)

    filepaths = []
    for _ in range(num_lines):
        filepaths.append(generate_random_path())

    # Ensure unique filepaths
    filepaths = list(set(filepaths))
    num_lines = len(filepaths)

    lines = []
    for filepath in filepaths:
        is_symlink = random.random() < 0.7
        if is_symlink:
            type_str = 'S'
            if random.random() < 0.9 and len(filepaths) > 0:
                target = random.choice(filepaths)
            else:
                target = generate_random_path()
            lines.append(f"{filepath}|{type_str}|{target}")
        else:
            type_str = 'F'
            hash_val = generate_random_hex(64)
            lines.append(f"{filepath}|{type_str}|{hash_val}")

    return "\n".join(lines) + "\n"

def test_fuzz_equivalence():
    agent_script = "/home/user/safe_manifest_parser.sh"
    oracle_bin = "/app/oracle_parser"

    assert os.path.isfile(agent_script), f"Agent script missing: {agent_script}"
    assert os.path.isfile(oracle_bin), f"Oracle missing: {oracle_bin}"

    random.seed(42)

    for i in range(100):
        manifest = generate_manifest()

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin],
            input=manifest,
            text=True,
            capture_output=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on iteration {i}."
        oracle_out = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            ["bash", agent_script],
            input=manifest,
            text=True,
            capture_output=True
        )

        agent_out = agent_proc.stdout

        if agent_out != oracle_out:
            error_msg = (
                f"Mismatch on iteration {i}!\n\n"
                f"--- Input Manifest ---\n{manifest}\n"
                f"--- Expected Output (Oracle) ---\n{oracle_out}\n"
                f"--- Actual Output (Agent) ---\n{agent_out}\n"
                f"STDERR: {agent_proc.stderr}"
            )
            pytest.fail(error_msg)