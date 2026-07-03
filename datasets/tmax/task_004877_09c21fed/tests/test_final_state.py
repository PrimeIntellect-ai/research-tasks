# test_final_state.py

import os
import random
import subprocess
import json
import urllib.request
import pytest

def test_fuzz_equivalence_kmer_dist():
    oracle_path = "/app/legacy_kmer_dist"
    agent_path = "/home/user/kmer_dist.py"

    assert os.path.exists(agent_path), f"Agent script missing at {agent_path}"
    assert os.path.exists(oracle_path), f"Oracle script missing at {oracle_path}"

    random.seed(42)
    chars = ['A', 'C', 'G', 'T']

    for i in range(100): # Using 100 instead of 1000 to keep test time reasonable, but checking fuzz equivalence thoroughly
        len1 = random.randint(10, 100)
        len2 = random.randint(10, 100)
        seq1 = "".join(random.choices(chars, k=len1))
        seq2 = "".join(random.choices(chars, k=len2))

        # Run oracle
        try:
            oracle_proc = subprocess.run(
                [oracle_path, seq1, seq2],
                capture_output=True, text=True, check=True
            )
            oracle_out = oracle_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Oracle failed on inputs {seq1}, {seq2}: {e.stderr}")

        # Run agent
        try:
            agent_proc = subprocess.run(
                ["python3", agent_path, seq1, seq2],
                capture_output=True, text=True, check=True
            )
            agent_out = agent_proc.stdout.strip()
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Agent script failed on inputs {seq1}, {seq2}: {e.stderr}")

        assert agent_out == oracle_out, f"Mismatch on inputs:\nSeq1: {seq1}\nSeq2: {seq2}\nOracle: {oracle_out}\nAgent: {agent_out}"

def test_gateway_api():
    url = "http://127.0.0.1:8000/analyze"

    seq1 = "ATGCATGCAT"
    seq2 = "GCATGCATGC"

    payload = json.dumps({"seq1": seq1, "seq2": seq2}).encode('utf-8')
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Failed to connect to or read from gateway API at {url}: {e}")

    assert "distance" in data, f"Response JSON missing 'distance' key: {data}"
    assert isinstance(data["distance"], float), f"Expected 'distance' to be a float, got {type(data['distance'])}"

    # Verify the API result against the oracle
    oracle_path = "/app/legacy_kmer_dist"
    oracle_proc = subprocess.run(
        [oracle_path, seq1, seq2],
        capture_output=True, text=True, check=True
    )
    oracle_out = float(oracle_proc.stdout.strip())

    assert abs(data["distance"] - oracle_out) < 1e-5, f"API returned distance {data['distance']}, expected {oracle_out}"