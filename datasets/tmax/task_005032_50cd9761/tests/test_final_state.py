# test_final_state.py

import os
import subprocess
import tempfile
import random
import string
import shutil
import pytest

ORACLE_PATH = "/app/legacy_archiver"
AGENT_PATH = "/home/user/archiver.sh"
NUM_ITERATIONS = 50

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_random_file(path, size=None):
    if size is None:
        size = random.randint(1, 1024)
    with open(path, 'wb') as f:
        f.write(os.urandom(size))

def create_test_environment(base_dir):
    data_dir = os.path.join(base_dir, "data")
    backup_base_dir = os.path.join(base_dir, "base_backup")
    os.makedirs(data_dir)
    os.makedirs(backup_base_dir)

    extensions = ['.txt', '.log', '.tmp', '.bak', '.bin']

    # Generate random directory tree
    num_files = random.randint(10, 50)
    dirs = [data_dir]

    for _ in range(random.randint(1, 5)):
        new_dir = os.path.join(random.choice(dirs), generate_random_string(5))
        os.makedirs(new_dir, exist_ok=True)
        dirs.append(new_dir)

    for _ in range(num_files):
        target_dir = random.choice(dirs)
        ext = random.choice(extensions)
        filename = f"{generate_random_string(6)}{ext}"
        filepath = os.path.join(target_dir, filename)

        # Decide if it's a file or symlink
        if random.random() < 0.1:
            # Create symlink
            target_file = os.path.join(data_dir, f"{generate_random_string(5)}.txt")
            create_random_file(target_file)
            os.symlink(target_file, filepath)
        else:
            create_random_file(filepath)

            # Decide if it exists in base_backup_dir
            rel_path = os.path.relpath(filepath, data_dir)
            base_filepath = os.path.join(backup_base_dir, rel_path)
            os.makedirs(os.path.dirname(base_filepath), exist_ok=True)

            rand_choice = random.random()
            if rand_choice < 0.3:
                # Exact copy (same size, same mtime)
                shutil.copy2(filepath, base_filepath)
            elif rand_choice < 0.6:
                # Different size/content
                create_random_file(base_filepath, size=random.randint(1025, 2048))

    # Generate config file
    config_path = os.path.join(base_dir, "config.ini")
    include_ext = ",".join(random.sample(extensions, random.randint(1, 3)))
    exclude_ext = ",".join(random.sample(extensions, random.randint(1, 2)))
    follow_symlinks = random.choice(["true", "false"])

    with open(config_path, "w") as f:
        f.write(f"include_ext={include_ext}\n")
        f.write(f"exclude_ext={exclude_ext}\n")
        f.write(f"base_backup_dir={backup_base_dir}\n")
        f.write(f"follow_symlinks={follow_symlinks}\n")

    return config_path, data_dir

def test_agent_script_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent script missing at {AGENT_PATH}"
    assert os.path.isfile(AGENT_PATH), f"Agent path {AGENT_PATH} is not a file"
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script {AGENT_PATH} is not executable"

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle binary missing at {ORACLE_PATH}"
    assert os.access(ORACLE_PATH, os.X_OK), f"Oracle binary {ORACLE_PATH} is not executable"

    random.seed(42)  # Fixed seed for reproducible fuzzing

    for i in range(NUM_ITERATIONS):
        with tempfile.TemporaryDirectory() as tmpdir:
            config_path, data_dir = create_test_environment(tmpdir)

            # Run oracle
            oracle_cmd = [ORACLE_PATH, config_path, data_dir]
            oracle_result = subprocess.run(oracle_cmd, capture_output=True, text=True)

            # Run agent
            agent_cmd = [AGENT_PATH, config_path, data_dir]
            agent_result = subprocess.run(agent_cmd, capture_output=True, text=True)

            # Compare
            oracle_stdout = oracle_result.stdout.strip()
            agent_stdout = agent_result.stdout.strip()

            if oracle_stdout != agent_stdout:
                with open(config_path, "r") as f:
                    config_contents = f.read()
                error_msg = (
                    f"Mismatch on iteration {i+1}!\n\n"
                    f"Config:\n{config_contents}\n"
                    f"Data Dir: {data_dir}\n\n"
                    f"Oracle Output:\n{oracle_stdout}\n\n"
                    f"Agent Output:\n{agent_stdout}\n"
                )
                pytest.fail(error_msg)