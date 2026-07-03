# test_final_state.py

import os
import random
import string
import subprocess
import shutil
import tempfile
import pytest

ORACLE_PATH = "/opt/oracle/analyzer_oracle"
AGENT_PATH = "/home/user/analyzer/target/release/analyzer"

def generate_random_filename():
    length = random.randint(5, 8)
    name = ''.join(random.choices(string.ascii_lowercase, k=length))
    return f"{name}.txt"

def create_random_tree(base_dir, num_files, max_depth, inject_cycle):
    dirs = [base_dir]
    for _ in range(random.randint(1, max_depth)):
        parent = random.choice(dirs)
        new_dir = os.path.join(parent, ''.join(random.choices(string.ascii_lowercase, k=5)))
        os.makedirs(new_dir, exist_ok=True)
        dirs.append(new_dir)

    files = []
    for _ in range(num_files):
        d = random.choice(dirs)
        fname = generate_random_filename()
        fpath = os.path.join(d, fname)
        files.append(fpath)
        with open(fpath, 'w') as f:
            pass

    edges = []
    for i in range(len(files)):
        num_deps = random.randint(0, 3)
        for _ in range(num_deps):
            if i + 1 < len(files):
                dep_idx = random.randint(i + 1, len(files) - 1)
                edges.append((i, dep_idx))

    if inject_cycle and len(files) >= 2:
        idx1 = random.randint(0, len(files) - 2)
        idx2 = random.randint(idx1 + 1, len(files) - 1)
        edges.append((idx2, idx1))

    for i in range(len(files)):
        deps = [files[j] for u, j in edges if u == i]
        with open(files[i], 'w') as f:
            for dep in deps:
                dep_name = os.path.basename(dep)
                f.write(f'include "{dep_name}"\n')

    return files

def test_executable_exists():
    assert os.path.isfile(AGENT_PATH), f"Agent executable not found at {AGENT_PATH}"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent executable at {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.isfile(ORACLE_PATH), f"Oracle executable not found at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle executable at {ORACLE_PATH} is not executable"

    random.seed(42)
    N = 50

    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(N):
            test_dir = os.path.join(temp_dir, f"test_{i}")
            os.makedirs(test_dir)

            num_files = random.randint(5, 15)
            max_depth = random.randint(1, 3)
            inject_cycle = random.random() < 0.05

            create_random_tree(test_dir, num_files, max_depth, inject_cycle)

            oracle_proc = subprocess.run([ORACLE_PATH, test_dir], capture_output=True, text=True)
            agent_proc = subprocess.run([AGENT_PATH, test_dir], capture_output=True, text=True)

            assert oracle_proc.returncode == agent_proc.returncode, (
                f"Return code mismatch on input {test_dir}.\n"
                f"Oracle: {oracle_proc.returncode}\nAgent: {agent_proc.returncode}\n"
                f"Oracle stdout: {oracle_proc.stdout}\nAgent stdout: {agent_proc.stdout}"
            )

            assert oracle_proc.stdout == agent_proc.stdout, (
                f"Output mismatch on input {test_dir}.\n"
                f"Oracle output:\n{oracle_proc.stdout}\n"
                f"Agent output:\n{agent_proc.stdout}\n"
            )