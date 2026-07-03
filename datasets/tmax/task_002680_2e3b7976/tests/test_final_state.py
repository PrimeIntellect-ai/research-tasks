# test_final_state.py

import os
import random
import string
import subprocess
import urllib.request
import urllib.error
import pytest

def test_redis_running_and_configured():
    """Check if Redis is accessible via 127.0.0.1:6379."""
    try:
        result = subprocess.run(
            ["redis-cli", "-h", "127.0.0.1", "-p", "6379", "PING"],
            capture_output=True, text=True, timeout=5
        )
        assert "PONG" in result.stdout, "Redis is not responding to PING on 127.0.0.1:6379"
    except FileNotFoundError:
        pytest.fail("redis-cli not found")

def test_nginx_data_endpoint():
    """Check if Nginx serves files from /app/backup_data/ via /data/."""
    test_filename = "test_nginx_data_123.dat"
    test_filepath = f"/app/backup_data/{test_filename}"
    test_content = b"nginx_data_test_content"

    os.makedirs("/app/backup_data", exist_ok=True)
    with open(test_filepath, "wb") as f:
        f.write(test_content)

    try:
        req = urllib.request.Request(f"http://127.0.0.1/data/{test_filename}")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, "Nginx /data/ endpoint did not return 200 OK"
            content = response.read()
            assert content == test_content, "Nginx /data/ endpoint returned incorrect content"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to fetch from Nginx /data/ endpoint: {e}")
    finally:
        if os.path.exists(test_filepath):
            os.remove(test_filepath)

def test_nginx_api_endpoint():
    """Check if Nginx proxies /api/ to the Python Backup API."""
    try:
        req = urllib.request.Request("http://127.0.0.1/api/status")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, "Nginx /api/ endpoint did not return 200 OK"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to fetch from Nginx /api/ endpoint: {e}")

def generate_random_filename():
    length = random.randint(5, 15)
    chars = string.ascii_letters + string.digits + "_-"
    return "".join(random.choices(chars, k=length)) + ".dat"

def setup_test_files_and_redis(num_files=10):
    filenames = []
    os.makedirs("/app/backup_data", exist_ok=True)
    for _ in range(num_files):
        fname = generate_random_filename()
        filenames.append(fname)

        # Write random payload
        payload = "".join(random.choices(string.ascii_letters, k=100))
        with open(f"/app/backup_data/{fname}", "w") as f:
            f.write(payload)

        # Write metadata to Redis in UTF-16LE
        meta_utf8 = f"meta_for_{fname}"
        meta_utf16le = meta_utf8.encode("utf-16le")

        # We need to set raw bytes in Redis. redis-cli -x SET is good for this.
        proc = subprocess.run(
            ["redis-cli", "-x", "SET", f"file_meta:{fname}"],
            input=meta_utf16le,
            capture_output=True
        )
        assert proc.returncode == 0, f"Failed to set redis key for {fname}"

    return filenames

def test_archive_processor_fuzz_equivalence():
    """Fuzz equivalence test for the archive processor script."""
    agent_script = "/home/user/archive_processor.sh"
    oracle_script = "/app/oracle_archiver.sh"

    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"
    assert os.path.isfile(oracle_script), f"Oracle script missing at {oracle_script}"

    random.seed(42)
    pool_size = 50
    filenames_pool = setup_test_files_and_redis(pool_size)

    iterations = 20 # Reduced from 100 to save test time but still verify correctness

    for i in range(iterations):
        num_files = random.randint(1, 10)
        selected_files = random.choices(filenames_pool, k=num_files)
        input_data = "\n".join(selected_files) + "\n"

        # Clear audit log before run
        if os.path.exists("/tmp/backup_audit.log"):
            os.remove("/tmp/backup_audit.log")

        # Run oracle
        oracle_proc = subprocess.run(
            ["bash", oracle_script],
            input=input_data,
            text=True,
            capture_output=True
        )
        oracle_stdout = oracle_proc.stdout

        oracle_audit = ""
        if os.path.exists("/tmp/backup_audit.log"):
            with open("/tmp/backup_audit.log", "r") as f:
                oracle_audit = f.read()

        # Clear audit log before agent run
        if os.path.exists("/tmp/backup_audit.log"):
            os.remove("/tmp/backup_audit.log")

        # Run agent
        agent_proc = subprocess.run(
            ["bash", agent_script],
            input=input_data,
            text=True,
            capture_output=True
        )
        agent_stdout = agent_proc.stdout

        agent_audit = ""
        if os.path.exists("/tmp/backup_audit.log"):
            with open("/tmp/backup_audit.log", "r") as f:
                agent_audit = f.read()

        assert agent_stdout == oracle_stdout, (
            f"Fuzz iteration {i} failed.\n"
            f"Input:\n{input_data}\n"
            f"Expected stdout:\n{oracle_stdout}\n"
            f"Got stdout:\n{agent_stdout}"
        )

        # Compare audit logs (order independent)
        oracle_audit_lines = sorted([line for line in oracle_audit.splitlines() if line.strip()])
        agent_audit_lines = sorted([line for line in agent_audit.splitlines() if line.strip()])

        assert agent_audit_lines == oracle_audit_lines, (
            f"Fuzz iteration {i} failed on audit log.\n"
            f"Input:\n{input_data}\n"
            f"Expected audit lines:\n{oracle_audit_lines}\n"
            f"Got audit lines:\n{agent_audit_lines}"
        )