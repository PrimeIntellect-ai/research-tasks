# test_final_state.py
import os
import redis
import pytest

def test_pipeline_script_exists():
    assert os.path.isfile("/home/user/workspace/pipeline.py"), "The script /home/user/workspace/pipeline.py does not exist."

def test_done_file_exists():
    assert os.path.isfile("/home/user/workspace/done"), "The file /home/user/workspace/done does not exist. Ensure you create it when finished."

def test_redis_fraud_scores_accuracy():
    golden_file = "/app/golden_top100.txt"
    assert os.path.isfile(golden_file), f"Golden truth file {golden_file} is missing from the environment."

    try:
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        r.ping()
    except redis.exceptions.ConnectionError:
        pytest.fail("Could not connect to Redis server on localhost:6379.")

    submitted = r.zrevrange('fraud_scores', 0, 99)
    assert len(submitted) > 0, "Redis sorted set 'fraud_scores' is empty or does not exist."

    with open(golden_file, 'r') as f:
        golden = [line.strip() for line in f.readlines() if line.strip()]

    assert len(golden) > 0, "Golden truth file is empty."

    overlap_count = len(set(submitted).intersection(set(golden)))
    accuracy = overlap_count / 100.0

    assert accuracy >= 0.95, f"Accuracy {accuracy:.2f} is below the threshold of 0.95. Only {overlap_count} out of 100 matched the golden set."