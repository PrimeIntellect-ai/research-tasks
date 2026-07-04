# test_final_state.py

import os
import json
import sys
import subprocess
import pytest

def test_bug_trigger_payload():
    """Verify that bug_trigger.json exists, is valid JSON, and contains a crashing payload."""
    path = '/home/user/bug_trigger.json'
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, 'r') as f:
        try:
            payload = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not valid JSON.")

    nodes = payload.get('nodes', [])
    assert isinstance(nodes, list) and len(nodes) > 0, "No nodes found in the JSON payload."

    triggers = False
    for node in nodes:
        m = node.get('metrics', {})
        b = m.get('base_score', 100)
        p = m.get('penalty', 0)
        l = m.get('latency_ms', 1)
        if b - p - l == 0:
            triggers = True
            break

    assert triggers, "bug_trigger.json does not contain metrics that would cause the divisor to be 0."

def test_health_aggregator_fixed_logic():
    """Verify that compute_score in health_aggregator.py handles zero division correctly."""
    sys.path.insert(0, '/home/user')
    try:
        import health_aggregator
    except ImportError:
        pytest.fail("Could not import /home/user/health_aggregator.py")

    # Test normal functionality is preserved
    normal_metrics = {'base_score': 100, 'penalty': 0, 'latency_ms': 50}
    try:
        score = health_aggregator.compute_score(normal_metrics)
        assert score == 20.0, f"Normal computation failed, expected 20.0, got {score}"
    except Exception as e:
        pytest.fail(f"compute_score raised an exception for normal metrics: {e}")

    # Test the bug condition is handled
    bug_metrics = {'base_score': 100, 'penalty': 50, 'latency_ms': 50}
    try:
        score_zero = health_aggregator.compute_score(bug_metrics)
        assert score_zero == 0, f"compute_score did not return 0 for zero divisor, got {score_zero}"
    except ZeroDivisionError:
        pytest.fail("compute_score still raises ZeroDivisionError when divisor is 0")
    except Exception as e:
        pytest.fail(f"compute_score raised an unexpected exception for bug metrics: {e}")

def test_health_aggregator_execution():
    """Verify that running the script with the bug_trigger.json exits with 0 and doesn't crash."""
    script_path = '/home/user/health_aggregator.py'
    payload_path = '/home/user/bug_trigger.json'

    if not os.path.exists(payload_path):
        pytest.skip("bug_trigger.json not found, skipping execution test.")

    result = subprocess.run(
        [sys.executable, script_path, payload_path],
        capture_output=True, text=True
    )

    assert result.returncode == 0, (
        f"health_aggregator.py exited with code {result.returncode}.\n"
        f"Stdout: {result.stdout}\nStderr: {result.stderr}"
    )

    assert "ZeroDivisionError" not in result.stdout, "health_aggregator.py stdout contains ZeroDivisionError."
    assert "ZeroDivisionError" not in result.stderr, "health_aggregator.py stderr contains ZeroDivisionError."