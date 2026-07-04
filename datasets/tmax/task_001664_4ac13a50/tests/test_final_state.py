# test_final_state.py
import os
import time
import json
import subprocess
import pytest
import math

def get_pg_container():
    out = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}", "--filter", "ancestor=postgres"])
    names = out.decode().strip().split('\n')
    return names[0] if names and names[0] else None

def get_redis_container():
    out = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}", "--filter", "ancestor=redis"])
    names = out.decode().strip().split('\n')
    return names[0] if names and names[0] else None

def run_db_query(query):
    pg_container = get_pg_container()
    if pg_container:
        cmd = ["docker", "exec", "-i", pg_container, "psql", "-U", "postgres", "-d", "sensors", "-t", "-c", query]
    else:
        cmd = ["psql", "-h", "localhost", "-U", "postgres", "-d", "sensors", "-t", "-c", query]

    env = os.environ.copy()
    env["PGPASSWORD"] = "secret"
    out = subprocess.check_output(cmd, env=env)
    return out.decode().strip()

def get_redis_queue_length():
    redis_container = get_redis_container()
    if redis_container:
        cmd = ["docker", "exec", "-i", redis_container, "redis-cli", "LLEN", "sensor:raw"]
    else:
        cmd = ["redis-cli", "-h", "localhost", "LLEN", "sensor:raw"]

    out = subprocess.check_output(cmd)
    return int(out.decode().strip())

def clear_redis_and_db():
    redis_container = get_redis_container()
    if redis_container:
        subprocess.check_call(["docker", "exec", "-i", redis_container, "redis-cli", "FLUSHALL"])
    else:
        subprocess.check_call(["redis-cli", "-h", "localhost", "FLUSHALL"])

    run_db_query("TRUNCATE cleaned_metrics;")

def get_all_metrics():
    out = run_db_query("SELECT id, z_score FROM cleaned_metrics ORDER BY id;")
    results = {}
    for line in out.split('\n'):
        line = line.strip()
        if not line:
            continue
        parts = line.split('|')
        if len(parts) == 2:
            results[int(parts[0].strip())] = float(parts[1].strip())
    return results

def test_processor_executable_exists():
    assert os.path.isfile("/home/user/processor"), "Go processor binary not found at /home/user/processor"
    assert os.access("/home/user/processor", os.X_OK), "/home/user/processor is not executable"

def test_processor_correctness_and_performance():
    # 1. Get Golden Truth
    clear_redis_and_db()
    subprocess.run(["python3", "/app/producer.py"], check=True)

    slow_proc = subprocess.Popen(["python3", "/app/slow_processor.py"])
    while True:
        if get_redis_queue_length() == 0:
            break
        time.sleep(0.5)
    slow_proc.terminate()
    slow_proc.wait()

    expected_metrics = get_all_metrics()
    assert len(expected_metrics) > 0, "Slow processor failed to write any metrics. Check setup."

    # 2. Test Go Processor
    clear_redis_and_db()
    subprocess.run(["python3", "/app/producer.py"], check=True)

    start_time = time.time()
    go_proc = subprocess.Popen(["/home/user/processor"])

    while True:
        if get_redis_queue_length() == 0:
            break
        time.sleep(0.05)

    end_time = time.time()
    go_proc.terminate()
    go_proc.wait()

    runtime = end_time - start_time

    actual_metrics = get_all_metrics()

    # 3. Assertions
    assert runtime <= 2.5, f"Runtime {runtime:.2f}s exceeds threshold of 2.5s"

    assert len(actual_metrics) == len(expected_metrics), f"Expected {len(expected_metrics)} rows, got {len(actual_metrics)}"

    mse = 0.0
    for k, expected_z in expected_metrics.items():
        assert k in actual_metrics, f"Missing id {k} in actual metrics"
        actual_z = actual_metrics[k]
        mse += (actual_z - expected_z) ** 2

    mse /= len(expected_metrics)
    assert mse <= 1e-5, f"MSE {mse:.2e} exceeds threshold of 1e-5"