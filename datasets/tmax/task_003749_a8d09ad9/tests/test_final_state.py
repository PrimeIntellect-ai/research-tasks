# test_final_state.py
import os
import random
import string
import hashlib
import subprocess
import shutil
import time
import pytest

def generate_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_fuzz_staging_dir(base_dir, num_records):
    os.makedirs(base_dir, exist_ok=True)
    manifest_lines = []

    for i in range(num_records):
        filename = f"{generate_random_string(random.randint(5, 15))}.ext"
        category = generate_random_string(random.randint(3, 10))

        # Decide if this record will be valid, corrupted hash, or missing file
        status = random.choices(['valid', 'corrupt', 'missing'], weights=[80, 10, 10])[0]

        file_content = os.urandom(random.randint(10, 100))
        actual_hash = hashlib.sha256(file_content).hexdigest()

        if status == 'corrupt':
            expected_hash = hashlib.sha256(os.urandom(10)).hexdigest()
        else:
            expected_hash = actual_hash

        manifest_lines.append(f"Filename: {filename}")
        manifest_lines.append(f"Category: {category}")
        manifest_lines.append(f"SHA256: {expected_hash}")
        manifest_lines.append("---")

        if status != 'missing':
            # Create file at random depth
            depth = random.randint(1, 5)
            current_dir = base_dir
            for _ in range(depth):
                subdir = generate_random_string(5)
                current_dir = os.path.join(current_dir, subdir)
                os.makedirs(current_dir, exist_ok=True)

            file_path = os.path.join(current_dir, filename)
            with open(file_path, 'wb') as f:
                f.write(file_content)

    manifest_path = os.path.join(base_dir, 'manifest.txt')
    with open(manifest_path, 'w') as f:
        f.write('\n'.join(manifest_lines) + '\n')

def test_pipeline_configs_fixed():
    nginx_conf = "/app/ingestion/nginx.conf"
    worker_env = "/app/ingestion/worker.env"

    assert os.path.exists(nginx_conf), f"Missing {nginx_conf}"
    with open(nginx_conf, 'r') as f:
        content = f.read()
    assert "127.0.0.1:5000" in content, "nginx.conf not updated to proxy_pass 127.0.0.1:5000"

    assert os.path.exists(worker_env), f"Missing {worker_env}"
    with open(worker_env, 'r') as f:
        content = f.read()
    assert "REDIS_PORT=6379" in content, "worker.env not updated to REDIS_PORT=6379"

def test_dataset_linker_fuzz_equivalence():
    agent_script = "/home/user/dataset_linker.sh"
    oracle_bin = "/app/oracle_linker"

    assert os.path.exists(agent_script), f"Missing {agent_script}"
    assert os.access(agent_script, os.X_OK), f"{agent_script} is not executable"

    random.seed(42)

    for i in range(100):
        fuzz_base = f"/tmp/fuzz_test_{i}"
        staging_dir = os.path.join(fuzz_base, "staging")
        agent_out = os.path.join(fuzz_base, "agent_out")
        oracle_out = os.path.join(fuzz_base, "oracle_out")

        if os.path.exists(fuzz_base):
            shutil.rmtree(fuzz_base)

        os.makedirs(agent_out)
        os.makedirs(oracle_out)

        num_records = random.randint(0, 50)
        create_fuzz_staging_dir(staging_dir, num_records)

        # Run oracle
        oracle_res = subprocess.run([oracle_bin, staging_dir, oracle_out], capture_output=True, text=True)
        assert oracle_res.returncode == 0, f"Oracle failed on iteration {i}"

        # Run agent
        agent_res = subprocess.run([agent_script, staging_dir, agent_out], capture_output=True, text=True)
        assert agent_res.returncode == 0, f"Agent script failed on iteration {i}. Stderr: {agent_res.stderr}"

        # Compare directories
        diff_res = subprocess.run(["diff", "-r", oracle_out, agent_out], capture_output=True, text=True)
        assert diff_res.returncode == 0, f"Output mismatch on iteration {i}:\n{diff_res.stdout}"

        # Check hardlinks
        for root, _, files in os.walk(agent_out):
            for file in files:
                agent_file = os.path.join(root, file)
                # Find the source file in staging
                source_found = False
                for src_root, _, src_files in os.walk(staging_dir):
                    if file in src_files:
                        src_file = os.path.join(src_root, file)
                        if os.stat(agent_file).st_ino == os.stat(src_file).st_ino:
                            source_found = True
                            break
                assert source_found, f"File {agent_file} is not a hardlink to the source file in staging"

        shutil.rmtree(fuzz_base)