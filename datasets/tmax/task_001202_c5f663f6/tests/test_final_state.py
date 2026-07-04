# test_final_state.py

import os
import sys
import subprocess
import tempfile
import random
import string
import json
import pytest

def test_toml_fixed_and_installed():
    """Verify that the toml package is fixed and installed correctly."""
    try:
        import toml
    except ImportError as e:
        pytest.fail(f"Failed to import 'toml'. Did you install it? Error: {e}")

    try:
        parsed = toml.loads('a = 1')
        assert parsed == {'a': 1}, "toml package did not parse correctly."
    except Exception as e:
        pytest.fail(f"toml package is still broken: {e}")

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_toml():
    artifact_name = generate_random_string(10)
    version = f"{random.randint(0, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}"
    architecture = random.choice(["amd64", "arm64", "x86", "armhf"])
    status = random.choice(["released", "beta", "alpha", "deprecated"])

    content = f"""[metadata]
artifact_name = "{artifact_name}"
version = "{version}"
architecture = "{architecture}"
status = "{status}"
"""
    return content

def create_fuzz_directory(base_dir):
    num_files = random.randint(5, 15)
    extensions = [".manifest", ".bin", ".txt"]
    encodings = ["utf-8", "utf-16le", "cp1252"]

    for i in range(num_files):
        ext = random.choice(extensions)
        filename = f"file_{i}_{generate_random_string(4)}{ext}"
        filepath = os.path.join(base_dir, filename)

        if ext == ".manifest":
            content = generate_random_toml()
            encoding = random.choice(encodings)
            with open(filepath, "w", encoding=encoding) as f:
                f.write(content)
        else:
            with open(filepath, "wb") as f:
                f.write(os.urandom(32))

def test_fuzz_equivalence():
    """Run fuzz equivalence testing between the oracle and the agent script."""
    oracle_path = "/app/oracle_curate"
    agent_script = "/home/user/curate.py"

    assert os.path.exists(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.exists(agent_script), f"Agent script not found at {agent_script}"

    N = 20
    random.seed(42)

    for i in range(N):
        with tempfile.TemporaryDirectory() as temp_dir:
            create_fuzz_directory(temp_dir)

            # Run oracle
            oracle_cmd = [oracle_path, temp_dir]
            try:
                oracle_res = subprocess.run(oracle_cmd, capture_output=True, text=True, check=True)
                oracle_out = oracle_res.stdout.strip()
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Oracle failed on input dir {temp_dir}. Error: {e.stderr}")

            # Run agent
            agent_cmd = [sys.executable, agent_script, temp_dir]
            try:
                agent_res = subprocess.run(agent_cmd, capture_output=True, text=True, check=True)
                agent_out = agent_res.stdout.strip()
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Agent script failed on input dir {temp_dir}. Error: {e.stderr}")

            if oracle_out != agent_out:
                pytest.fail(
                    f"Mismatch found on fuzz iteration {i}.\n"
                    f"Input directory contents: {os.listdir(temp_dir)}\n"
                    f"Oracle output:\n{oracle_out}\n\n"
                    f"Agent output:\n{agent_out}\n"
                )