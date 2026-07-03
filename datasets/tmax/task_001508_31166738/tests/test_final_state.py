# test_final_state.py
import os
import pytest

def calculate_metric(agent_file, ref_file):
    try:
        with open(agent_file, 'r') as f:
            agent_lines = set([line.strip() for line in f if line.strip()])
        with open(ref_file, 'r') as f:
            ref_lines = set([line.strip() for line in f if line.strip()])

        intersection = len(agent_lines.intersection(ref_lines))
        union = len(agent_lines.union(ref_lines))
        if union == 0:
            return 0.0
        return float(intersection) / float(union)
    except Exception:
        return 0.0

def test_output_jaccard_similarity():
    agent_file = '/home/user/output.csv'
    ref_file = '/tmp/reference_output.csv'

    assert os.path.exists(agent_file), f"Agent output file not found at {agent_file}"
    assert os.path.exists(ref_file), f"Reference file not found at {ref_file}"

    score = calculate_metric(agent_file, ref_file)
    assert score >= 0.99, f"Jaccard similarity score {score} is below the threshold of 0.99"

def test_log_masker_makefile_fixed():
    makefile_path = "/app/log-masker-1.0.0/Makefile"
    if os.path.isfile(makefile_path):
        with open(makefile_path, 'r') as f:
            content = f.read()
        assert "-Werrror" not in content, "The Makefile typo '-Werrror' was not fixed."