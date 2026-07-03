# test_final_state.py

import os
import struct
import random
import subprocess
import tempfile
import shutil
import pytest

AGENT_EXECUTABLE = "/home/user/safe_unpacker"
ORACLE_EXECUTABLE = "/app/oracle_unpacker"

def generate_fuzz_archive(filepath, seed):
    rng = random.Random(seed)
    with open(filepath, 'wb') as f:
        f.write(b'CARC')
        num_files = rng.randint(0, 15)
        for _ in range(num_files):
            path_type = rng.choice(['normal', 'traversal_unix', 'traversal_win', 'absolute_unix', 'absolute_win', 'mixed'])
            if path_type == 'normal':
                name = f"dir{rng.randint(1,5)}/file{rng.randint(1,1000)}.bin"
            elif path_type == 'traversal_unix':
                name = f"../../file{rng.randint(1,1000)}.bin"
            elif path_type == 'traversal_win':
                name = f"..\\..\\file{rng.randint(1,1000)}.bin"
            elif path_type == 'absolute_unix':
                name = f"/etc/shadow{rng.randint(1,1000)}"
            elif path_type == 'absolute_win':
                name = f"C:\\Windows\\System32\\cmd{rng.randint(1,1000)}.exe"
            else:
                name = f"dir1/../dir2/..\\..\\file{rng.randint(1,1000)}.bin"

            name_bytes = name.encode('utf-16le')
            f.write(struct.pack('<H', len(name_bytes)))
            f.write(name_bytes)

            content_len = rng.randint(0, 512)
            content = rng.randbytes(content_len)
            f.write(struct.pack('<I', content_len))
            f.write(content)

def get_dir_state(d):
    state = {}
    for root, dirs, files in os.walk(d):
        for file in files:
            p = os.path.join(root, file)
            rel = os.path.relpath(p, d)
            with open(p, 'rb') as f:
                state[rel] = f.read()
    return state

def test_agent_executable_exists():
    assert os.path.isfile(AGENT_EXECUTABLE), f"Agent executable not found at {AGENT_EXECUTABLE}"
    assert os.access(AGENT_EXECUTABLE, os.X_OK), f"Agent executable is not executable: {AGENT_EXECUTABLE}"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_EXECUTABLE), f"Oracle executable not found at {ORACLE_EXECUTABLE}"

    num_tests = 1000

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(num_tests):
            archive_path = os.path.join(tmpdir, f"archive_{i}.bin")
            generate_fuzz_archive(archive_path, seed=i)

            oracle_dir = os.path.join(tmpdir, f"oracle_ext_{i}")
            agent_dir = os.path.join(tmpdir, f"agent_ext_{i}")
            os.makedirs(oracle_dir)
            os.makedirs(agent_dir)

            oracle_res = subprocess.run([ORACLE_EXECUTABLE, archive_path, oracle_dir], capture_output=True, text=True)
            agent_res = subprocess.run([AGENT_EXECUTABLE, archive_path, agent_dir], capture_output=True, text=True)

            # Compare stdout (warnings)
            oracle_stdout = oracle_res.stdout.strip()
            agent_stdout = agent_res.stdout.strip()

            # The agent might format warnings slightly differently, but let's check directory state strictly
            oracle_state = get_dir_state(oracle_dir)
            agent_state = get_dir_state(agent_dir)

            if oracle_state != agent_state:
                oracle_files = list(oracle_state.keys())
                agent_files = list(agent_state.keys())
                pytest.fail(
                    f"Mismatch on fuzz input {i} (seed={i}).\n"
                    f"Oracle extracted files: {oracle_files}\n"
                    f"Agent extracted files: {agent_files}\n"
                    f"Oracle stdout:\n{oracle_stdout}\n"
                    f"Agent stdout:\n{agent_stdout}\n"
                )