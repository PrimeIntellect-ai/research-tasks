# test_final_state.py

import os
import json
import pytest
import requests

def test_fasta_file_exists():
    """Ensure the target FASTA file exists and contains the correct sequence."""
    fasta_path = "/home/user/target.fasta"
    assert os.path.isfile(fasta_path), f"FASTA file is missing at {fasta_path}"

    with open(fasta_path, "r") as f:
        lines = f.readlines()

    # Filter out header lines (starting with '>') and join the sequence
    sequence = "".join(line.strip() for line in lines if not line.startswith(">"))
    assert "ACDFG" in sequence, f"Expected sequence 'ACDFG' not found in {fasta_path}. Found: {sequence}"

def test_simulation_endpoint_target_fasta():
    """Test the /simulate endpoint with the target FASTA file."""
    url = "http://127.0.0.1:8080/simulate"
    payload = {
        "fasta_path": "/home/user/target.fasta",
        "iterations": 500000
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "mean_sq_dist" in data, f"'mean_sq_dist' missing from response: {data}"

    mean_sq_dist = data["mean_sq_dist"]
    assert isinstance(mean_sq_dist, (int, float)), f"'mean_sq_dist' should be a number, got {type(mean_sq_dist)}"
    assert 54.5 <= mean_sq_dist <= 55.5, f"Expected mean_sq_dist to be between 54.5 and 55.5, got {mean_sq_dist}"

def test_simulation_endpoint_adversarial_fasta(tmp_path):
    """Test the /simulate endpoint with a temporary adversarial FASTA file."""
    fasta_path = tmp_path / "test.fasta"
    fasta_path.write_text(">Adversarial\nAAACCC\n")

    url = "http://127.0.0.1:8080/simulate"
    payload = {
        "fasta_path": str(fasta_path),
        "iterations": 500000
    }

    try:
        response = requests.post(url, json=payload, timeout=15)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "mean_sq_dist" in data, f"'mean_sq_dist' missing from response: {data}"

    mean_sq_dist = data["mean_sq_dist"]
    assert isinstance(mean_sq_dist, (int, float)), f"'mean_sq_dist' should be a number, got {type(mean_sq_dist)}"
    assert 14.5 <= mean_sq_dist <= 15.5, f"Expected mean_sq_dist to be between 14.5 and 15.5, got {mean_sq_dist}"