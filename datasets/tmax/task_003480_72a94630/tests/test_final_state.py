# test_final_state.py

import os
import time
import subprocess
import json
import pytest

BINARY_PATH = "/home/user/biocore_sim/target/release/biocore_sim"
VIDEO_PATH = "/app/reaction_video.mp4"
FASTA_PATH = "/app/reference.fasta"
RESULTS_PATH = "/home/user/results.json"

def test_binary_exists():
    """Check if the release binary was compiled."""
    assert os.path.isfile(BINARY_PATH), f"Release binary not found at {BINARY_PATH}. Did you run 'cargo build --release'?"

def test_execution_time_and_accuracy():
    """Run the binary, measure execution time, and validate the output accuracy."""
    # Ensure a fresh run by removing any existing results.json
    if os.path.exists(RESULTS_PATH):
        os.remove(RESULTS_PATH)

    start_time = time.time()
    result = subprocess.run(
        [BINARY_PATH, VIDEO_PATH, FASTA_PATH, RESULTS_PATH],
        capture_output=True,
        text=True
    )
    end_time = time.time()
    duration = end_time - start_time

    assert result.returncode == 0, f"Program exited with code {result.returncode}.\nStderr: {result.stderr}"
    assert os.path.isfile(RESULTS_PATH), f"Results file not found at {RESULTS_PATH}"

    with open(RESULTS_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    cq = data.get("cq_value")
    dna = data.get("final_dna_concentration")
    score = data.get("max_alignment_score")

    assert cq is not None, "Missing 'cq_value' in results.json"
    assert dna is not None, "Missing 'final_dna_concentration' in results.json"
    assert score is not None, "Missing 'max_alignment_score' in results.json"

    # Accuracy checks
    assert abs(cq - 12.8) <= 0.1, f"Accuracy failed: cq_value {cq} is not within 0.1 of 12.8"
    assert abs(dna - 0.92) <= 0.01, f"Accuracy failed: final_dna_concentration {dna} is not within 0.01 of 0.92"
    assert score == 156, f"Accuracy failed: max_alignment_score {score} does not equal 156"

    # Performance check
    assert duration <= 1.5, f"Performance failed: Execution time {duration:.3f}s exceeds the 1.5s threshold"