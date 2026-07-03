# test_final_state.py
import json
import redis
import pytest
from scipy.stats import kstest

def test_ingestion_script_fixed():
    """Verify that the Flask ingestion script was patched with correct host and port."""
    with open('/app/ingestion.py', 'r') as f:
        content = f.read()

    assert "6379" in content, "Redis port in ingestion.py was not fixed to 6379."
    assert "127.0.0.1" in content or "0.0.0.0" in content, "Flask host in ingestion.py was not fixed to a valid loopback/any address."

def test_redis_data_and_distribution():
    """Verify that Redis contains the generated data and it matches the target normal distribution."""
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
        # Attempt a ping to ensure connection is actually established
        r.ping()
    except redis.exceptions.ConnectionError:
        pytest.fail("Could not connect to Redis on 127.0.0.1:6379. Is redis-server running?")

    data = r.lrange('graph_metrics', 0, -1)
    assert data, "No data found in Redis list 'graph_metrics'."

    values = []
    for d in data:
        try:
            parsed = json.loads(d)
            values.append(float(parsed['c']))
        except (json.JSONDecodeError, KeyError, ValueError):
            pytest.fail(f"Data in Redis is not in the expected JSON format {{'c': <value>}}. Found: {d}")

    assert len(values) >= 10000, f"Expected at least 10000 values in Redis, but found {len(values)}."

    # Use exactly 10,000 samples for deterministic KS test bounds
    values = values[:10000]

    # Compute Kolmogorov-Smirnov D-statistic against N(0.30, 0.05^2)
    stat, pval = kstest(values, 'norm', args=(0.30, 0.05))

    assert stat < 0.03, (
        f"KS_STAT is {stat:.4f}, which is not < 0.03. "
        "The distribution of the generated clustering coefficients does not "
        "sufficiently match the target N(0.30, 0.05^2)."
    )