# test_final_state.py

import os
import pytest

PIPELINE_DIR = "/home/user/pipeline"
SLOWEST_STEP_FILE = "/home/user/slowest_step.txt"
GRAPH_OUTPUT_FILE = os.path.join(PIPELINE_DIR, "graph_output.txt")
FILTERED_SEQ_FILE = os.path.join(PIPELINE_DIR, "filtered_sequences.txt")

def test_slowest_step_identified():
    assert os.path.isfile(SLOWEST_STEP_FILE), f"File {SLOWEST_STEP_FILE} does not exist."
    with open(SLOWEST_STEP_FILE, "r") as f:
        content = f.read().strip()
    assert content == "step3_graph_build.sh", f"Expected 'step3_graph_build.sh' in {SLOWEST_STEP_FILE}, got '{content}'"

def test_graph_output_exists():
    assert os.path.isfile(GRAPH_OUTPUT_FILE), f"File {GRAPH_OUTPUT_FILE} does not exist. Did you run the orchestrator?"

def test_graph_output_correctness():
    assert os.path.isfile(FILTERED_SEQ_FILE), f"File {FILTERED_SEQ_FILE} does not exist."

    # Read filtered sequences
    with open(FILTERED_SEQ_FILE, "r") as f:
        sequences = [line.strip() for line in f if line.strip()]

    # Compute expected edges
    expected_edges = set()
    for s1 in sequences:
        for s2 in sequences:
            if s1 != s2:
                if s1[-4:] == s2[:4]:
                    expected_edges.add(f"{s1} -> {s2}")

    # Read actual edges
    actual_edges = set()
    with open(GRAPH_OUTPUT_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                actual_edges.add(line)

    missing = expected_edges - actual_edges
    extra = actual_edges - expected_edges

    assert not missing, f"Missing {len(missing)} expected edges in {GRAPH_OUTPUT_FILE}. Example: {list(missing)[0]}"
    assert not extra, f"Found {len(extra)} extra edges in {GRAPH_OUTPUT_FILE}. Example: {list(extra)[0]}"