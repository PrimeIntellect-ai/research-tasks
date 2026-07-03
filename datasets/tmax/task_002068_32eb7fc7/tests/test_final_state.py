# test_final_state.py

import os
import pytest

APP_DIR = "/home/user/app"
OBSERVATIONS_FILE = "/home/user/app/observations.csv"
OPT_EXEC_FILE = "/home/user/app/mesh_align_opt"
OUTPUT_FILE = "/home/user/app/top_nodes.txt"
PRIMER = "ATGCGTACGTTAGC"

def compute_expected_top_nodes():
    """Derive the expected top 5 nodes by reading the CSV and applying the scoring logic."""
    if not os.path.isfile(OBSERVATIONS_FILE):
        pytest.fail(f"Missing observations file: {OBSERVATIONS_FILE}")

    nodes = []
    with open(OBSERVATIONS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(',')
            if len(parts) >= 4:
                node_id = int(parts[0])
                seq = parts[3]

                # Compute score
                score = 0
                for i in range(min(len(PRIMER), len(seq))):
                    if PRIMER[i] == seq[i]:
                        score += 10

                nodes.append((node_id, score))

    # Sort by score descending, then by node_id to ensure stable comparison if needed
    # The C code uses bubble sort which is stable, but ties might be ordered differently depending on the sort implementation used by the student.
    # We will just collect the top 5 scores.
    nodes.sort(key=lambda x: x[1], reverse=True)
    return nodes[:5]

def test_optimized_executable_exists():
    assert os.path.isfile(OPT_EXEC_FILE), f"Optimized executable {OPT_EXEC_FILE} is missing."
    assert os.access(OPT_EXEC_FILE, os.X_OK), f"File {OPT_EXEC_FILE} is not executable."

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} is missing. Did you run the optimized executable?"

def test_output_file_contents():
    expected_top = compute_expected_top_nodes()

    with open(OUTPUT_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 5, f"Expected exactly 5 lines in {OUTPUT_FILE}, found {len(lines)}."

    parsed_output = []
    for line in lines:
        # Expected format: "NodeID: 402, Score: 850"
        parts = line.split(',')
        assert len(parts) == 2, f"Line format incorrect: {line}"

        id_part = parts[0].strip()
        score_part = parts[1].strip()

        assert id_part.startswith("NodeID:"), f"Expected 'NodeID:' in line: {line}"
        assert score_part.startswith("Score:"), f"Expected 'Score:' in line: {line}"

        try:
            node_id = int(id_part.split(':')[1].strip())
            score = int(score_part.split(':')[1].strip())
        except ValueError:
            pytest.fail(f"Could not parse integer from line: {line}")

        parsed_output.append((node_id, score))

    # Compare the top 5. Since there could be ties, we check if the set of (id, score) matches
    # or if the scores match and the IDs are among the valid top ones.
    expected_set = set(expected_top)
    actual_set = set(parsed_output)

    # If the exact set matches, we are good.
    if expected_set == actual_set:
        return

    # If not exact match, check if the scores are correct and valid for the top 5.
    # Because there might be multiple nodes with the same score, we just ensure the scores match the top 5 scores
    # and the IDs actually have those scores.
    expected_scores = sorted([x[1] for x in expected_top], reverse=True)
    actual_scores = sorted([x[1] for x in parsed_output], reverse=True)

    assert actual_scores == expected_scores, f"Expected top 5 scores {expected_scores}, but got {actual_scores}."

    # Verify each outputted node actually has that score
    all_nodes = {}
    with open(OBSERVATIONS_FILE, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if len(parts) >= 4:
                all_nodes[int(parts[0])] = parts[3]

    for node_id, score in parsed_output:
        assert node_id in all_nodes, f"NodeID {node_id} not found in observations."
        seq = all_nodes[node_id]
        actual_score = sum(10 for i in range(min(len(PRIMER), len(seq))) if PRIMER[i] == seq[i])
        assert actual_score == score, f"NodeID {node_id} has actual score {actual_score}, but output claims {score}."