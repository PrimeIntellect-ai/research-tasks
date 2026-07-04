# test_final_state.py

import os
import pytest

def test_metrics_file_exists():
    assert os.path.isfile('/home/user/metrics.txt'), "The file /home/user/metrics.txt does not exist."

def test_pipeline_script_exists():
    assert os.path.isfile('/home/user/pipeline.sh'), "The script /home/user/pipeline.sh does not exist."

def test_metric_threshold():
    metrics_path = '/home/user/metrics.txt'
    assert os.path.isfile(metrics_path), "The file /home/user/metrics.txt does not exist."

    with open(metrics_path, 'r') as f:
        content = f.read().strip()

    assert 'Test_Similarity:' in content, "The format 'Test_Similarity: <score>' was not found in metrics.txt."

    try:
        score_str = content.split('Test_Similarity:')[1].strip()
        agent_score = float(score_str)
    except Exception as e:
        pytest.fail(f"Failed to parse the score from metrics.txt: {e}")

    target_score = 0.824
    error = abs(agent_score - target_score)
    tolerance = 0.05

    assert error <= tolerance, f"Metric threshold failed: Agent score {agent_score} is not within {tolerance} of target {target_score} (Error: {error})"