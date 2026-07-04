# test_final_state.py
import os
import json
import random
import string
import subprocess
import tempfile
import shutil
import pytest

def generate_random_file(path, size):
    with open(path, 'wb') as f:
        f.write(os.urandom(size))

def create_random_directory_structure(base_dir, num_files, max_depth=3):
    extensions = ['.txt', '.log', '.tmp', '.dat', '.bin', '.csv']
    dirs = [base_dir]

    # Create some subdirectories
    for depth in range(max_depth):
        new_dirs = []
        for d in dirs:
            for _ in range(random.randint(0, 2)):
                sub = os.path.join(d, ''.join(random.choices(string.ascii_letters, k=5)))
                os.makedirs(sub, exist_ok=True)
                new_dirs.append(sub)
        dirs.extend(new_dirs)

    all_files = []
    # Create files
    for _ in range(num_files):
        d = random.choice(dirs)
        ext = random.choice(extensions)
        name = ''.join(random.choices(string.ascii_letters, k=8)) + ext
        filepath = os.path.join(d, name)
        size = random.randint(0, 1024 * 100) # 0 to 100KB for faster tests
        generate_random_file(filepath, size)
        all_files.append(filepath)

    # Create symlinks
    num_symlinks = random.randint(0, 5)
    for _ in range(num_symlinks):
        if not all_files:
            break
        target = random.choice(all_files)
        d = random.choice(dirs)
        linkname = ''.join(random.choices(string.ascii_letters, k=8)) + ".lnk"
        linkpath = os.path.join(d, linkname)
        if not os.path.exists(linkpath):
            os.symlink(target, linkpath)

    # Create hard links
    num_hardlinks = random.randint(0, 5)
    for _ in range(num_hardlinks):
        if not all_files:
            break
        target = random.choice(all_files)
        d = random.choice(dirs)
        linkname = ''.join(random.choices(string.ascii_letters, k=8)) + ".hlnk"
        linkpath = os.path.join(d, linkname)
        if not os.path.exists(linkpath):
            os.link(target, linkpath)

    return extensions

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_backup_tool"
    agent_path = "/home/user/new_backup_tool.py"

    assert os.path.exists(oracle_path), f"Oracle not found at {oracle_path}"
    assert os.path.exists(agent_path), f"Agent script not found at {agent_path}"

    random.seed(42)

    num_tests = 50
    with tempfile.TemporaryDirectory() as temp_base:
        for i in range(num_tests):
            test_dir = os.path.join(temp_base, f"fuzz_dir_{i}")
            os.makedirs(test_dir)

            num_files = random.randint(5, 25)
            available_exts = create_random_directory_structure(test_dir, num_files)

            config = {
                "ignore_extensions": random.sample(available_exts, random.randint(0, min(3, len(available_exts)))),
                "follow_symlinks": random.choice([True, False]),
                "extract_header_bytes": random.randint(0, 64)
            }

            config_path = os.path.join(temp_base, f"config_{i}.json")
            with open(config_path, 'w') as f:
                json.dump(config, f)

            # Run oracle
            try:
                oracle_result = subprocess.run(
                    [oracle_path, config_path, test_dir],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=10,
                    check=True
                )
                oracle_out = oracle_result.stdout
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Oracle failed on test {i}: {e.stderr.decode('utf-8', errors='ignore')}")

            # Run agent
            try:
                agent_result = subprocess.run(
                    ["python3", agent_path, config_path, test_dir],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=10,
                    check=True
                )
                agent_out = agent_result.stdout
            except subprocess.CalledProcessError as e:
                pytest.fail(f"Agent failed on test {i}: {e.stderr.decode('utf-8', errors='ignore')}")

            assert oracle_out == agent_out, (
                f"Mismatch on test {i}!\n"
                f"Config: {config}\n"
                f"Directory: {test_dir}\n"
                f"Oracle output length: {len(oracle_out)}, Agent output length: {len(agent_out)}\n"
                "Outputs differ bit-for-bit."
            )