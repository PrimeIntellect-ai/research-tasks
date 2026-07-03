# test_final_state.py

import os
import pytest
import requests

def get_expected_populations(fasta_path):
    populations = {}
    if not os.path.exists(fasta_path):
        return populations

    with open(fasta_path, 'r') as f:
        seq_id = None
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq_id:
                    s = "".join(seq)
                    gc = sum(1 for c in s if c in 'GCgc')
                    r = gc / len(s) if len(s) > 0 else 0
                    P = 10.0
                    for _ in range(10):
                        P += r * P * (1 - P / 100.0)
                    populations[seq_id] = P
                seq_id = line[1:]
                seq = []
            else:
                seq.append(line)
        if seq_id:
            s = "".join(seq)
            gc = sum(1 for c in s if c in 'GCgc')
            r = gc / len(s) if len(s) > 0 else 0
            P = 10.0
            for _ in range(10):
                P += r * P * (1 - P / 100.0)
            populations[seq_id] = P
    return populations

def test_process_script_exists():
    """Verify that the user created the process.sh script."""
    script_path = "/home/user/process.sh"
    assert os.path.isfile(script_path), f"Missing file: {script_path} was not created."

def test_api_responses():
    """Verify that the API is running and returning the correct population values."""
    fasta_path = "/home/user/sequences.fasta"
    assert os.path.isfile(fasta_path), f"Missing FASTA file: {fasta_path}"

    expected_pops = get_expected_populations(fasta_path)
    assert expected_pops, "No sequences found to test."

    for seq_id, expected_p in expected_pops.items():
        url = f"http://127.0.0.1:8080/api/population?seq_id={seq_id}"
        try:
            resp = requests.get(url, timeout=5)
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to API for {seq_id} at {url}. Is the Flask app running? Error: {e}")

        assert resp.status_code == 200, f"Expected HTTP 200 for {seq_id}, got {resp.status_code}. Response: {resp.text}"

        try:
            data = resp.json()
        except ValueError:
            pytest.fail(f"API did not return valid JSON for {seq_id}. Response: {resp.text}")

        assert "population" in data, f"Response for {seq_id} missing 'population' key. JSON: {data}"

        actual_p = data["population"]
        expected_rounded = round(expected_p, 2)

        # The API rounds to 2 decimal places, and bash tools might have slight float differences
        assert abs(actual_p - expected_rounded) <= 0.05, (
            f"Population mismatch for {seq_id}. "
            f"Expected approx {expected_rounded}, got {actual_p}."
        )