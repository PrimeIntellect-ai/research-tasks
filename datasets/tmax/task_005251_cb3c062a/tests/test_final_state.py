# test_final_state.py
import redis
import pytest

def test_redis_payload_count():
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        # Verify connection and get keys
        r.ping()
        count = len(r.keys('payload:*'))
    except redis.exceptions.ConnectionError:
        pytest.fail("Failed to connect to Redis on localhost:6379. Ensure the Redis server is running.")
    except Exception as e:
        pytest.fail(f"An error occurred while communicating with Redis: {e}")

    threshold = 9999
    assert count == threshold, f"Metric threshold failed: Expected exactly {threshold} payloads in Redis, but found {count}."