# test_final_state.py
import os
import pytest

def evaluate(agent_file, golden_file):
    try:
        with open(agent_file, 'r') as f:
            agent_lines = [l.strip() for l in f.readlines() if l.strip()]
    except FileNotFoundError:
        return 0.0

    with open(golden_file, 'r') as f:
        golden_lines = [l.strip() for l in f.readlines() if l.strip()]

    if not golden_lines:
        return 0.0

    # Calculate intersection and accuracy
    agent_set = set(agent_lines)
    golden_set = set(golden_lines)

    correct = len(agent_set.intersection(golden_set))

    # Exact sequence match is preferred, but we will measure F1 on line content
    precision = correct / len(agent_set) if agent_set else 0
    recall = correct / len(golden_set) if golden_set else 0

    if precision + recall == 0:
        return 0.0

    f1 = 2 * (precision * recall) / (precision + recall)

    # Require lines to be in the original order
    if agent_lines == golden_lines:
        f1 = 1.0
    elif f1 == 1.0:
        # Sets match but order doesn't
        f1 = 0.99 

    return f1

def test_filtered_log_accuracy():
    """Evaluate the filtered log against the golden reference file using F1 score."""
    agent_file = '/home/user/filtered.log'
    golden_file = '/app/golden_filtered.log'

    assert os.path.exists(agent_file), f"Agent output file not found: {agent_file}"
    assert os.path.exists(golden_file), f"Golden reference file not found: {golden_file}"

    score = evaluate(agent_file, golden_file)
    assert score >= 1.0, f"Filtered log accuracy (F1 score) is {score:.4f}, expected 1.0 for an exact match. Ensure logs are filtered correctly and in the original order."

def test_script_exists_and_executable():
    """Ensure the user's script exists and is executable."""
    script_path = '/home/user/filter_logs.sh'
    assert os.path.isfile(script_path), f"Script not found: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"