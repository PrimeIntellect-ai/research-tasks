# test_final_state.py
import os
import random
import string
import subprocess
import sqlite3
import urllib.request
import json
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/legacy_processor.bin"
    agent_path = "/home/user/processor.py"

    assert os.path.isfile(oracle_path), f"Oracle binary missing at {oracle_path}"
    assert os.path.isfile(agent_path), f"Agent script missing at {agent_path}"

    random.seed(42)
    printable = string.printable

    for _ in range(1000):
        length = random.randint(0, 256)
        input_str = "".join(random.choice(printable) for _ in range(length))

        oracle_proc = subprocess.run([oracle_path, input_str], capture_output=True, text=True)
        agent_proc = subprocess.run(["python3", agent_path, input_str], capture_output=True, text=True)

        assert oracle_proc.returncode == agent_proc.returncode, f"Return codes differ for input: {repr(input_str)}"
        assert oracle_proc.stdout == agent_proc.stdout, f"Output differs for input: {repr(input_str)}\nOracle: {repr(oracle_proc.stdout)}\nAgent: {repr(agent_proc.stdout)}"

def test_database_recovery():
    db_path = "/app/metrics_recovered.db"
    assert os.path.isfile(db_path), f"Recovered database not found at {db_path}"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, value FROM metrics WHERE id = 1")
        row = cursor.fetchone()
        assert row is not None, "Metric ID 1 not found in recovered DB"
        assert row[1] == 10, f"Expected metric value 10, got {row[1]}"
    except sqlite3.DatabaseError as e:
        pytest.fail(f"Recovered database is invalid or corrupted: {e}")
    finally:
        conn.close()

def test_flask_and_redis_orchestration():
    # Test Flask endpoint
    url = "http://127.0.0.1:5000/process?id=1"
    try:
        req = urllib.request.urlopen(url, timeout=5)
        res = req.read().decode("utf-8")
        data = json.loads(res)
    except Exception as e:
        pytest.fail(f"Failed to query Flask app at {url}: {e}")

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert "result" in data, "Expected 'result' in response"

    # Test Redis cache
    try:
        import redis
        r = redis.Redis(host="127.0.0.1", port=6379, db=0)
        cached_val = r.get("metric_1")
        assert cached_val is not None, "Result not cached in Redis under key 'metric_1'"
        assert int(cached_val) == data["result"], f"Cached value {cached_val} does not match API result {data['result']}"
    except ImportError:
        pytest.fail("redis library not installed")
    except Exception as e:
        pytest.fail(f"Failed to verify Redis cache: {e}")