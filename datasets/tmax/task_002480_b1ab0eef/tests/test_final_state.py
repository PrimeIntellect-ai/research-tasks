# test_final_state.py
import os
import json
import difflib
import pytest

def test_updated_config_similarity():
    """Test that the updated configuration matches the expected target using string similarity."""
    expected_dict = {
        "max_retries": 5,
        "db_password": "***",
        "cache_size": 1024,
        "listen_port": 80
    }

    config_path = '/home/user/updated_config.json'
    assert os.path.exists(config_path), f"Updated config file missing: {config_path}"

    try:
        with open(config_path, 'r') as f:
            agent_data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to load {config_path} as JSON: {e}")

    expected_str = json.dumps(expected_dict, sort_keys=True, separators=(',', ':'))

    # Ensure types match (e.g. if STT captured '5' as string vs int, cast gracefully for comparison)
    for k in list(agent_data.keys()):
        if k in ["max_retries", "cache_size", "listen_port"]:
            try: 
                agent_data[k] = int(agent_data[k])
            except (ValueError, TypeError):
                pass

    agent_str = json.dumps(agent_data, sort_keys=True, separators=(',', ':'))

    score = difflib.SequenceMatcher(None, expected_str, agent_str).ratio()

    assert score >= 0.90, f"Similarity Score: {score} is below threshold 0.90. Agent JSON: {agent_str}"

def test_drift_file_exists_and_integer():
    """Test that the drift score file exists and contains an integer."""
    drift_path = '/home/user/drift.txt'
    assert os.path.exists(drift_path), f"Drift file missing: {drift_path}"

    with open(drift_path, 'r') as f:
        content = f.read().strip()

    assert content, "Drift file is empty."

    try:
        int(content)
    except ValueError:
        pytest.fail(f"Drift file does not contain a valid integer. Found: '{content}'")