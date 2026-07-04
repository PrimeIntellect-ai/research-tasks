# test_final_state.py

import os
import time
import gzip
import random
import string
import shutil
import tempfile
import subprocess
import urllib.request
import urllib.error

AGENT_SCRIPT = "/home/user/process_artifact.py"
ORACLE_SCRIPT = "/opt/verifier/oracle_process_artifact.py"

def generate_fuzz_content(size):
    chars = string.ascii_letters + string.digits
    content = "".join(random.choices(chars, k=size))
    # Insert __MACRO_REPO_HOST__ randomly
    num_insertions = random.randint(1, 10)
    for _ in range(num_insertions):
        pos = random.randint(0, len(content))
        content = content[:pos] + "__MACRO_REPO_HOST__" + content[pos:]
    return content.encode('utf-8')

def test_agent_script_exists():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script {AGENT_SCRIPT} is missing."

def test_fuzz_equivalence():
    random.seed(42)
    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(20):
            # Keep size reasonable for test speed: 10KB to 100KB
            size = random.randint(10000, 100000)
            content = generate_fuzz_content(size)

            orig_path = os.path.join(tmpdir, f"orig_{i}.gz")
            with gzip.open(orig_path, 'wb') as f:
                f.write(content)

            oracle_path = os.path.join(tmpdir, f"oracle_{i}.gz")
            agent_path = os.path.join(tmpdir, f"agent_{i}.gz")

            shutil.copy(orig_path, oracle_path)
            shutil.copy(orig_path, agent_path)

            # Run oracle
            subprocess.run(["python3", ORACLE_SCRIPT, oracle_path], check=True)

            # Run agent
            res = subprocess.run(["python3", AGENT_SCRIPT, agent_path], capture_output=True, text=True)
            assert res.returncode == 0, f"Agent script failed on input {i}. Stderr: {res.stderr}"

            # Compare results
            with gzip.open(oracle_path, 'rb') as f:
                oracle_content = f.read()
            with gzip.open(agent_path, 'rb') as f:
                agent_content = f.read()

            assert agent_content == oracle_content, f"Mismatch on fuzz input {i}. Agent output did not match oracle."

def test_start_worker_configured():
    script_path = "/app/start_worker.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    with open(script_path, "r") as f:
        content = f.read()
    assert "PROCESSOR_SCRIPT=/home/user/process_artifact.py" in content, f"{script_path} does not export PROCESSOR_SCRIPT correctly."

def test_services_running():
    # Check Redis
    res = subprocess.run(["pgrep", "-f", "redis-server"], capture_output=True)
    assert res.returncode == 0, "Redis server is not running."

    # Check Flask
    res = subprocess.run(["pgrep", "-f", "upload_server.py"], capture_output=True)
    assert res.returncode == 0, "Flask upload_server.py is not running."

    # Check Worker
    res = subprocess.run(["pgrep", "-f", "worker.py"], capture_output=True)
    assert res.returncode == 0, "Worker daemon is not running."

def test_end_to_end_flow():
    content = b"Some random text with __MACRO_REPO_HOST__ inside."
    expected_content = b"Some random text with artifact-repo.internal.srv inside."

    with tempfile.NamedTemporaryFile(suffix=".gz", delete=False) as tmp:
        with gzip.open(tmp.name, 'wb') as f:
            f.write(content)
        tmp_path = tmp.name

    filename = os.path.basename(tmp_path)

    # Post file to flask app
    with open(tmp_path, 'rb') as f:
        data = f.read()

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
        "Content-Type: application/gzip\r\n\r\n"
    ).encode('utf-8') + data + f"\r\n--{boundary}--\r\n".encode('utf-8')

    req = urllib.request.Request("http://127.0.0.1:5000/upload", data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

    try:
        urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to upload file to Flask service: {e}")

    # Wait for worker to process
    upload_dir = "/home/user/uploads"
    target_file = os.path.join(upload_dir, filename)

    success = False
    for _ in range(50):
        if os.path.exists(target_file):
            try:
                with gzip.open(target_file, 'rb') as f:
                    processed = f.read()
                if processed == expected_content:
                    success = True
                    break
            except Exception:
                pass
        time.sleep(0.1)

    assert success, "End-to-end flow failed: file was not processed correctly within the timeout."