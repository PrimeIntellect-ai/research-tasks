# test_final_state.py
import os
import json
import pytest

MEASUREMENTS_FILE = "/home/user/measurements.csv"
WELFORD_FILE = "/home/user/welford_stats.jsonl"
POSTERIOR_FILE = "/home/user/bayesian_posterior.json"

@pytest.fixture(scope="module")
def expected_stats():
    if not os.path.isfile(MEASUREMENTS_FILE):
        pytest.fail(f"Input file {MEASUREMENTS_FILE} is missing.")

    n = 0
    mean = 0.0
    M2 = 0.0
    sum_x = 0.0

    welford_stats = []

    with open(MEASUREMENTS_FILE, "r") as f:
        for line in f:
            val = line.strip()
            if not val:
                continue
            x = float(val)
            n += 1
            sum_x += x

            delta = x - mean
            mean += delta / n
            delta2 = x - mean
            M2 += delta * delta2

            if n % 1000 == 0:
                variance = M2 / (n - 1) if n > 1 else 0.0
                welford_stats.append({
                    "n": n,
                    "mean": round(mean, 3),
                    "variance": round(variance, 3)
                })

    post_var = 1.0 / (1.0 + n)
    post_mean = post_var * sum_x

    posterior_stats = {
        "posterior_mean": round(post_mean, 5),
        "posterior_variance": round(post_var, 5)
    }

    return welford_stats, posterior_stats

def test_welford_stats_file(expected_stats):
    """Test that the welford_stats.jsonl file contains correct intermediate statistics."""
    expected_welford, _ = expected_stats

    assert os.path.isfile(WELFORD_FILE), f"The file {WELFORD_FILE} is missing."

    with open(WELFORD_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(expected_welford), f"Expected {len(expected_welford)} lines in {WELFORD_FILE}, found {len(lines)}."

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {WELFORD_FILE} is not valid JSON: {line}")

        expected = expected_welford[i]
        assert "n" in data and data["n"] == expected["n"], f"Line {i+1} missing or incorrect 'n'. Expected {expected['n']}."
        assert "mean" in data and data["mean"] == expected["mean"], f"Line {i+1} incorrect 'mean'. Expected {expected['mean']}, got {data.get('mean')}."
        assert "variance" in data and data["variance"] == expected["variance"], f"Line {i+1} incorrect 'variance'. Expected {expected['variance']}, got {data.get('variance')}."

def test_bayesian_posterior_file(expected_stats):
    """Test that the bayesian_posterior.json file contains correct final posterior statistics."""
    _, expected_posterior = expected_stats

    assert os.path.isfile(POSTERIOR_FILE), f"The file {POSTERIOR_FILE} is missing."

    with open(POSTERIOR_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {POSTERIOR_FILE} is not valid JSON.")

    assert "posterior_mean" in data, f"Key 'posterior_mean' missing in {POSTERIOR_FILE}."
    assert "posterior_variance" in data, f"Key 'posterior_variance' missing in {POSTERIOR_FILE}."

    assert data["posterior_mean"] == expected_posterior["posterior_mean"], \
        f"Incorrect posterior_mean. Expected {expected_posterior['posterior_mean']}, got {data['posterior_mean']}."

    assert data["posterior_variance"] == expected_posterior["posterior_variance"], \
        f"Incorrect posterior_variance. Expected {expected_posterior['posterior_variance']}, got {data['posterior_variance']}."