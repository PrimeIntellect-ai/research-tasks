# test_final_state.py

import os
import subprocess
import requests
import pytest
import re

def test_aligner_compiled():
    aligner_path = "/app/aligner"
    assert os.path.isfile(aligner_path), f"Executable not found at {aligner_path}"
    assert os.access(aligner_path, os.X_OK), f"File at {aligner_path} is not executable"

def get_fasta_dict(filepath):
    sequences = {}
    with open(filepath, 'r') as f:
        header = None
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if header:
                    sequences[header] = "".join(seq)
                header = line[1:]
                seq = []
            else:
                seq.append(line)
        if header:
            sequences[header] = "".join(seq)
    return sequences

def test_http_server_and_logic():
    aligner_path = "/app/aligner"

    # 1. Recompute the expected highest score
    db_seqs = get_fasta_dict("/app/database.fasta")
    ref_seq = db_seqs.get("seq_8492")
    assert ref_seq, "Reference sequence >seq_8492 not found in database.fasta"

    query_seqs = get_fasta_dict("/app/queries.fasta")

    best_query = None
    best_score = -float('inf')

    for q_header, q_seq in query_seqs.items():
        try:
            result = subprocess.run([aligner_path, ref_seq, q_seq], capture_output=True, text=True, check=True)
            score = int(result.stdout.strip())
            if score > best_score:
                best_score = score
                best_query = q_header
        except Exception as e:
            pytest.fail(f"Failed to run {aligner_path} or parse its output: {e}")

    expected_body = f"{best_query}:{best_score}"

    # 2. Test HTTP server
    url = "http://127.0.0.1:9090/result"

    # Test without auth
    try:
        resp = requests.get(url, timeout=2)
        assert resp.status_code == 401, f"Expected 401 Unauthorized without auth, got {resp.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP server not responding or error without auth: {e}")

    # Test with bad auth
    try:
        resp = requests.get(url, headers={"Authorization": "Bearer 1234"}, timeout=2)
        assert resp.status_code == 401, f"Expected 401 Unauthorized with bad auth, got {resp.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP server error with bad auth: {e}")

    # Test with correct auth
    try:
        resp = requests.get(url, headers={"Authorization": "Bearer 8492"}, timeout=2)
        assert resp.status_code == 200, f"Expected 200 OK with correct auth, got {resp.status_code}"
        assert resp.text.strip() == expected_body, f"Expected response body '{expected_body}', got '{resp.text.strip()}'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"HTTP server error with correct auth: {e}")