# test_final_state.py
import os
import pandas as pd
import pytest

def test_results_accuracy():
    agent_file = '/home/user/results.csv'
    golden_file = '/tmp/golden.csv'

    assert os.path.exists(agent_file), f"Agent results file not found at {agent_file}"
    assert os.path.exists(golden_file), f"Golden results file not found at {golden_file}"

    try:
        golden = pd.read_csv(golden_file, names=['src', 'dst', 'dist'])
    except Exception as e:
        pytest.fail(f"Failed to read golden file: {e}")

    try:
        agent = pd.read_csv(agent_file, names=['src', 'dst', 'dist'])
    except Exception as e:
        pytest.fail(f"Failed to read agent results file: {e}")

    assert not golden.empty, "Golden file is empty."
    assert not agent.empty, "Agent results file is empty."

    merged = golden.merge(agent, on=['src', 'dst'], suffixes=('_gold', '_agent'))

    assert len(merged) == len(golden), (
        f"Agent results missing some queries or format is incorrect. "
        f"Expected {len(golden)} matching queries, found {len(merged)}."
    )

    correct = (merged['dist_gold'] == merged['dist_agent']).sum()
    accuracy = correct / len(golden)

    assert accuracy >= 1.0, f"Accuracy is {accuracy:.2f}, expected >= 1.0. Correct: {correct}/{len(golden)}"