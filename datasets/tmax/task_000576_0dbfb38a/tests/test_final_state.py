# test_final_state.py

import time
import subprocess
import redis
import pytest

def test_extract_graph_performance_and_correctness():
    # 1. Clear Redis
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    r.flushall()

    # 2. Run agent script and time it
    start = time.time()
    result = subprocess.run(["python", "/app/extract_graph.py"], capture_output=True)
    end = time.time()
    runtime = end - start

    # 3. Validate script executed successfully
    assert result.returncode == 0, f"Script failed with error: {result.stderr.decode('utf-8', errors='ignore')}"

    # 4. Validate correctness of Redis keys
    keys = r.keys("author:*:score")
    assert len(keys) > 0, "No author score keys found in Redis. The script did not populate the expected data."

    # Check a sample key for correct structure
    sample_key = keys[0]
    author_id = sample_key.split(":")[1]

    score_val = r.get(sample_key)
    assert score_val is not None
    try:
        float_val = float(score_val)
    except ValueError:
        pytest.fail(f"Score value '{score_val}' for key {sample_key} is not a valid float.")

    cites_key = f"author:{author_id}:cites"
    key_type = r.type(cites_key)
    if key_type != 'none':
        assert key_type == 'set', f"Expected {cites_key} to be a Redis Set, got {key_type}"

    # 5. Assert the metric (execution time) against the threshold
    assert runtime <= 2.5, f"Execution time {runtime:.3f}s exceeded the threshold of 2.5s. The script is not efficient enough."