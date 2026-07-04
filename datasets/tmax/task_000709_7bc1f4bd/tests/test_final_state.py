# test_final_state.py

import os
import subprocess
import random
import tempfile
import urllib.request
import json
import time
import pytest

def test_extracted_payload():
    payload_path = "/home/user/extracted_payload.bin"
    assert os.path.isfile(payload_path), f"Missing {payload_path}"

    # Check size
    assert os.path.getsize(payload_path) == 1024, "Extracted payload should be exactly 1024 bytes"

def test_makefile_and_artifacts():
    assert os.path.isfile("/home/user/Makefile"), "Makefile is missing"
    assert os.path.isfile("/home/user/decoder_cli"), "decoder_cli is missing"
    assert os.access("/home/user/decoder_cli", os.X_OK), "decoder_cli is not executable"
    assert os.path.isfile("/home/user/libdecoder.so"), "libdecoder.so is missing"
    assert os.path.isfile("/home/user/api.py"), "api.py is missing"

def test_fuzz_equivalence():
    oracle = "/app/oracle_decoder"
    agent = "/home/user/decoder_cli"

    assert os.path.isfile(oracle), "Oracle missing"
    assert os.path.isfile(agent), "Agent executable missing"

    random.seed(42)

    # We run 100 iterations to avoid test timeout while still providing strong coverage
    # (10000 subprocess calls would likely timeout standard test runners)
    N = 100

    with tempfile.TemporaryDirectory() as tmpdir:
        for i in range(N):
            input_file = os.path.join(tmpdir, f"input_{i}.bin")

            # Generate random binary files with 8-byte chunks
            # Length between 8 and 8000 bytes for test speed
            num_chunks = random.randint(1, 1000)
            data = bytearray()
            for _ in range(num_chunks):
                chunk_id = random.randint(0, 65535)
                total_chunks = random.randint(0, 65535)
                payload = random.randbytes(4)
                data.extend(chunk_id.to_bytes(2, 'little'))
                data.extend(total_chunks.to_bytes(2, 'little'))
                data.extend(payload)

            # Sometimes truncate to make it incomplete
            if random.random() < 0.1:
                data = data[:-random.randint(1, 7)]

            with open(input_file, "wb") as f:
                f.write(data)

            oracle_proc = subprocess.run([oracle, input_file], capture_output=True, text=True)
            agent_proc = subprocess.run([agent, input_file], capture_output=True, text=True)

            assert oracle_proc.returncode == agent_proc.returncode, f"Return code mismatch on input {input_file}"
            assert oracle_proc.stdout == agent_proc.stdout, f"Stdout mismatch on input {input_file}\nOracle:\n{oracle_proc.stdout}\nAgent:\n{agent_proc.stdout}"

def test_api_endpoint():
    # Start the API in the background if it's not already running
    # The user might not have left it running, so we'll try to start it using their Makefile
    proc = subprocess.Popen(["make", "start-api"], cwd="/home/user", stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Wait for API to start
        api_up = False
        for _ in range(20):
            try:
                with urllib.request.urlopen("http://localhost:8080/requests", timeout=1) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode())
                        assert isinstance(data, list), "API should return a JSON array"
                        api_up = True
                        break
            except Exception:
                time.sleep(0.5)

        assert api_up, "API did not start or did not return 200 OK at /requests"
    finally:
        proc.terminate()
        proc.wait()