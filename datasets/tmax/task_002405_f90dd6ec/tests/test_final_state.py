# test_final_state.py

import os
import random
import string
import subprocess
import tarfile
import tempfile
import filecmp
import pytest

ORACLE_PATH = "/test/oracle/safe_extract_oracle.sh"
AGENT_PATH = "/home/user/safe_extract.sh"

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits + " ", k=length))

def create_random_tar(tar_path, seed):
    random.seed(seed)
    num_files = random.randint(5, 15)

    with tarfile.open(tar_path, "w") as tar:
        for i in range(num_files):
            # Decide if zip-slip
            is_zip_slip = random.random() < 0.3
            is_conf = random.random() < 0.5

            filename = generate_random_string(10)
            if is_conf:
                filename += ".conf"
            else:
                filename += ".txt"

            if is_zip_slip:
                if random.random() < 0.5:
                    path = f"../../{generate_random_string(5)}/{filename}"
                else:
                    path = f"/{generate_random_string(5)}/{filename}"
            else:
                path = f"{generate_random_string(5)}/{filename}"

            # Content
            if is_conf:
                lines = []
                for _ in range(random.randint(3, 10)):
                    if random.random() < 0.3:
                        lines.append(f"  # {generate_random_string(20)}")
                    else:
                        lines.append(f"{generate_random_string(20)}")
                content = "\n".join(lines).encode('iso-8859-1')
            else:
                content = generate_random_string(50).encode('utf-8')

            # Create a temporary file to add to tar
            fd, temp_file_path = tempfile.mkstemp()
            with os.fdopen(fd, 'wb') as f:
                f.write(content)

            tar.add(temp_file_path, arcname=path)
            os.remove(temp_file_path)

def compare_directories(dir1, dir2):
    dcmp = filecmp.dircmp(dir1, dir2)
    if dcmp.left_only or dcmp.right_only or dcmp.diff_files:
        return False, f"Diff: left_only={dcmp.left_only}, right_only={dcmp.right_only}, diff_files={dcmp.diff_files}"

    for common_dir in dcmp.common_dirs:
        match, msg = compare_directories(os.path.join(dir1, common_dir), os.path.join(dir2, common_dir))
        if not match:
            return False, msg

    # Check file contents
    for common_file in dcmp.common_files:
        f1 = os.path.join(dir1, common_file)
        f2 = os.path.join(dir2, common_file)
        with open(f1, 'rb') as file1, open(f2, 'rb') as file2:
            if file1.read() != file2.read():
                return False, f"File content mismatch: {common_file}"

    return True, ""

def test_agent_exists_and_executable():
    assert os.path.exists(AGENT_PATH), f"Agent script {AGENT_PATH} not found."
    assert os.access(AGENT_PATH, os.X_OK), f"Agent script {AGENT_PATH} is not executable."

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle script {ORACLE_PATH} not found."

    num_iterations = 50
    for i in range(num_iterations):
        with tempfile.TemporaryDirectory() as tmpdir:
            tar_path = os.path.join(tmpdir, "fuzz_archive.tar")
            create_random_tar(tar_path, seed=42 + i)

            dest_oracle = os.path.join(tmpdir, "dest_oracle")
            dest_agent = os.path.join(tmpdir, "dest_agent")
            os.makedirs(dest_oracle)
            os.makedirs(dest_agent)

            # Run oracle
            oracle_proc = subprocess.run(
                [ORACLE_PATH, tar_path, dest_oracle],
                capture_output=True, text=True
            )

            # Run agent
            agent_proc = subprocess.run(
                [AGENT_PATH, tar_path, dest_agent],
                capture_output=True, text=True
            )

            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Iteration {i}: Return code mismatch. Oracle: {oracle_proc.returncode}, Agent: {agent_proc.returncode}\n"
                f"Agent stderr: {agent_proc.stderr}"
            )

            match, msg = compare_directories(dest_oracle, dest_agent)
            assert match, (
                f"Iteration {i}: Output directories do not match exactly.\n"
                f"Details: {msg}\n"
                f"Oracle stdout: {oracle_proc.stdout}\n"
                f"Agent stdout: {agent_proc.stdout}\n"
                f"Agent stderr: {agent_proc.stderr}"
            )