# test_final_state.py
import os
import subprocess
import tempfile
import random
import string
import zipfile
import tarfile
import json
import shutil
import pytest

ORACLE_PATH = "/opt/oracle/process_datasets_oracle"
AGENT_SRC = "/home/user/process_datasets.go"
AGENT_BIN = "/home/user/process_datasets"
OUTPUT_DIR = "/home/user/output"
INDEX_FILE = os.path.join(OUTPUT_DIR, "dataset_index.jsonl")

def setup_module():
    if os.path.exists(AGENT_SRC) and not os.path.exists(AGENT_BIN):
        subprocess.run(["go", "build", "-o", AGENT_BIN, AGENT_SRC], check=True)

def random_string(min_len=10, max_len=50):
    length = random.randint(min_len, max_len)
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def create_dat_content():
    return f"{random_string(5, 20)}\n{random_string(10, 50)}".encode('utf-8')

def create_archive(path, archive_type, traversal=False, nested_level=0):
    files_to_add = []

    if nested_level > 0:
        nested_path = path + f".nested.{archive_type}"
        create_archive(nested_path, archive_type, traversal, nested_level - 1)
        with open(nested_path, 'rb') as f:
            files_to_add.append((f"nested_{nested_level}.{archive_type}", f.read(), 0o644))
        os.remove(nested_path)

    if traversal:
        files_to_add.append((f"../../../../tmp/evil_{random_string(5)}.txt", b"malicious", 0o644))

    # Valid dat
    files_to_add.append((f"valid_{random_string(5)}.dat", create_dat_content(), 0o400))
    # Invalid dat (empty)
    files_to_add.append((f"empty_{random_string(5)}.dat", b"", 0o644))

    if archive_type == "zip":
        with zipfile.ZipFile(path, 'w') as zf:
            for name, content, perms in files_to_add:
                info = zipfile.ZipInfo(name)
                info.external_attr = (perms & 0xFFFF) << 16
                zf.writestr(info, content)
    elif archive_type == "tar.gz":
        with tarfile.open(path, 'w:gz') as tf:
            for name, content, perms in files_to_add:
                info = tarfile.TarInfo(name)
                info.size = len(content)
                info.mode = perms
                with tempfile.NamedTemporaryFile('wb', delete=False) as tmp:
                    tmp.write(content)
                    tmp_name = tmp.name
                tf.add(tmp_name, arcname=name)
                os.remove(tmp_name)

def generate_fuzz_case(work_dir, seed):
    random.seed(seed)
    log_path = os.path.join(work_dir, f"metadata_{seed}.log")

    num_records = random.randint(1, 5)
    records = []

    for i in range(num_records):
        archive_type = random.choice(["zip", "tar.gz"])
        traversal = random.random() < 0.3
        nested = random.randint(1, 3) if random.random() < 0.2 else 0

        archive_path = os.path.join(work_dir, f"archive_{seed}_{i}.{archive_type}")
        create_archive(archive_path, archive_type, traversal, nested)

        dataset_type = "verified_sensor_data" if random.random() < 0.8 else "other_data"

        record = f"""START_RECORD
Archive: {archive_path}
Dataset-Type: {dataset_type}
Description: {random_string(10, 100)}
END_RECORD"""
        records.append(record)

    with open(log_path, 'w') as f:
        f.write("\n".join(records) + "\n")

    return log_path

def run_program(bin_path, log_path):
    if os.path.exists(INDEX_FILE):
        os.remove(INDEX_FILE)

    result = subprocess.run([bin_path, log_path], capture_output=True, text=True)

    index_content = []
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    index_content.append(json.loads(line))
        # Sort for deterministic comparison
        index_content.sort(key=lambda x: (x.get("archive", ""), x.get("file", "")))

    return result.returncode, index_content

def test_fuzz_equivalence():
    assert os.path.exists(ORACLE_PATH), f"Oracle missing at {ORACLE_PATH}"
    assert os.path.exists(AGENT_BIN), f"Agent binary missing at {AGENT_BIN}. Did it compile?"

    num_fuzz_cases = 20

    with tempfile.TemporaryDirectory() as work_dir:
        for i in range(num_fuzz_cases):
            log_path = generate_fuzz_case(work_dir, i)

            oracle_code, oracle_index = run_program(ORACLE_PATH, log_path)
            agent_code, agent_index = run_program(AGENT_BIN, log_path)

            assert agent_code == oracle_code, f"Return code mismatch on case {i}. Oracle: {oracle_code}, Agent: {agent_code}"
            assert agent_index == oracle_index, f"Index output mismatch on case {i}.\nOracle: {oracle_index}\nAgent: {agent_index}"

def test_vendored_package_fixed():
    # Check if the vulnerability logic was restored
    zip_go = "/app/vendored/archiver/zip.go"
    tar_go = "/app/vendored/archiver/tar.go"

    assert os.path.exists(zip_go)
    assert os.path.exists(tar_go)

    # We just check if they compile and don't contain the obvious commented out strings if we want, 
    # but the fuzz equivalence test implicitly tests the behavior.
    with open(zip_go, 'r') as f:
        content = f.read()
        assert "illegal file path" in content or "fmt.Errorf" in content, "zip.go doesn't seem to have the error fix"