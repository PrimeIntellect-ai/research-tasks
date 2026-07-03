# test_final_state.py

import os
import random
import string
import struct
import subprocess
import tempfile
import pytest

ORACLE_PATH = "/app/oracle_extractor"
AGENT_PATH = "/home/user/extractor"

def generate_random_path():
    components = []
    num_components = random.randint(1, 5)
    for _ in range(num_components):
        choice = random.choice(["normal", "dot", "dotdot"])
        if choice == "normal":
            length = random.randint(1, 10)
            comp = "".join(random.choices(string.ascii_letters + string.digits, k=length))
            components.append(comp)
        elif choice == "dot":
            components.append(".")
        elif choice == "dotdot":
            components.append("..")

    # Sometimes start with a leading slash or dotdot
    if random.random() < 0.2:
        components.insert(0, "..")
    if random.random() < 0.1:
        components.insert(0, "")

    return "/".join(components)

def generate_rarc_archive(filepath):
    num_entries = random.randint(0, 20)
    with open(filepath, "wb") as f:
        f.write(b"RARC")
        for _ in range(num_entries):
            path = generate_random_path()
            path_bytes = path.encode("utf-8")
            path_len = len(path_bytes)
            # 16-bit little endian
            f.write(struct.pack("<H", path_len))
            f.write(path_bytes)

            data_size = random.randint(0, 1024)
            # 32-bit little endian
            f.write(struct.pack("<I", data_size))
            f.write(os.urandom(data_size))

def generate_target_dir():
    components = [""]
    num_components = random.randint(1, 4)
    for _ in range(num_components):
        length = random.randint(3, 8)
        comp = "".join(random.choices(string.ascii_letters, k=length))
        components.append(comp)
    return "/".join(components)

def test_extractor_equivalence():
    assert os.path.isfile(AGENT_PATH), f"Agent binary not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent binary at {AGENT_PATH} is not executable"

    assert os.path.isfile(ORACLE_PATH), f"Oracle binary not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary at {ORACLE_PATH} is not executable"

    random.seed(42)
    N = 500

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N):
            archive_path = os.path.join(tmpdir, f"archive_{i}.rarc")
            generate_rarc_archive(archive_path)
            target_dir = generate_target_dir()

            oracle_proc = subprocess.run(
                [ORACLE_PATH, archive_path, target_dir],
                capture_output=True,
                text=True
            )

            agent_proc = subprocess.run(
                [AGENT_PATH, archive_path, target_dir],
                capture_output=True,
                text=True
            )

            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Mismatch in return code on test {i}.\n"
                f"Archive: {archive_path}\nTarget Dir: {target_dir}\n"
                f"Oracle exit code: {oracle_proc.returncode}\n"
                f"Agent exit code: {agent_proc.returncode}\n"
                f"Oracle stderr: {oracle_proc.stderr}\n"
                f"Agent stderr: {agent_proc.stderr}"
            )

            assert agent_proc.stdout == oracle_proc.stdout, (
                f"Mismatch in stdout on test {i}.\n"
                f"Archive: {archive_path}\nTarget Dir: {target_dir}\n"
                f"Oracle stdout:\n{oracle_proc.stdout}\n"
                f"Agent stdout:\n{agent_proc.stdout}\n"
            )