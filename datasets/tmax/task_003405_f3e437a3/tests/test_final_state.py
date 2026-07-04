# test_final_state.py
import json
import os
import pytest

def test_results_file_exists():
    assert os.path.isfile('/tmp/results.json'), "Agent failed: /tmp/results.json not found. Did the pipeline script run and forward data?"

def test_results_format_and_count():
    results = []
    with open('/tmp/results.json', 'r') as f:
        for line in f:
            if line.strip():
                try:
                    data = json.loads(line)
                    results.append(data)
                except json.JSONDecodeError:
                    pytest.fail("Agent failed: /tmp/results.json contains invalid JSON lines.")

    assert len(results) >= 5, f"Agent failed: Not enough windows submitted ({len(results)} < 5). Ensure the pipeline runs for at least 60 seconds."

    for r in results:
        assert "window_start" in r, "Agent failed: 'window_start' key missing in result payload."
        assert "avg_temp" in r, "Agent failed: 'avg_temp' key missing in result payload."

def test_mse_metric():
    assert os.path.isfile('/app/ground_truth.json'), "Verifier error: missing /app/ground_truth.json"

    with open('/app/ground_truth.json', 'r') as f:
        truth = {int(k): float(v) for k, v in json.load(f).items()}

    results = []
    with open('/tmp/results.json', 'r') as f:
        for line in f:
            if line.strip():
                results.append(json.loads(line))

    mse = 0.0
    matched = 0
    for r in results:
        w_start = r.get("window_start")
        a_temp = r.get("avg_temp")
        if w_start in truth:
            diff = truth[w_start] - a_temp
            mse += diff * diff
            matched += 1

    assert matched > 0, "Agent failed: No matching window_starts found between results and ground truth."

    mse = mse / matched
    assert mse <= 0.5, f"Agent failed: MSE ({mse:.4f}) is greater than the threshold (0.5). Matched windows: {matched}."