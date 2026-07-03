# test_final_state.py
import time
import subprocess
import json
import pytest

def test_execution_time_and_redis_output():
    # Measure execution time
    start = time.time()
    proc = subprocess.run(["python3", "/app/backup_extractor.py", "45"], capture_output=True, text=True)
    duration = time.time() - start

    assert proc.returncode == 0, f"Script failed with error: {proc.stderr}"
    assert duration <= 0.5, f"Execution time {duration:.3f}s exceeded 0.5s threshold."

    # Fetch result from Redis
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        result_str = r.get("restore_chain:45")
    except ImportError:
        # Fallback if redis-py is not available, use redis-cli
        redis_proc = subprocess.run(["redis-cli", "GET", "restore_chain:45"], capture_output=True, text=True)
        result_str = redis_proc.stdout.strip()
        if result_str == "(nil)":
            result_str = None

    assert result_str is not None, "Redis key 'restore_chain:45' is missing."

    try:
        actual_ids = json.loads(result_str)
    except json.JSONDecodeError:
        pytest.fail(f"Redis value is not valid JSON: {result_str}")

    # Compute expected result using psql
    sql_query = """
    WITH RECURSIVE traverse AS (
        SELECT bj.id, bj.job_name, bj.status, bj.created_at
        FROM backup_jobs bj
        WHERE bj.id = 45
        UNION
        SELECT bj.id, bj.job_name, bj.status, bj.created_at
        FROM backup_jobs bj
        JOIN job_dependencies jd ON jd.child_job_id = bj.id
        JOIN traverse t ON t.id = jd.parent_job_id
    )
    SELECT id FROM (
        SELECT id, created_at, ROW_NUMBER() OVER(PARTITION BY job_name ORDER BY created_at DESC) as rn
        FROM traverse
    ) sub
    WHERE rn = 1
    ORDER BY created_at ASC;
    """

    psql_cmd = [
        "psql", "-U", "postgres", "-d", "backups",
        "-t", "-A", "-c", sql_query
    ]
    psql_proc = subprocess.run(psql_cmd, capture_output=True, text=True)
    assert psql_proc.returncode == 0, f"Failed to query database for expected results: {psql_proc.stderr}"

    expected_ids = []
    for line in psql_proc.stdout.strip().split('\n'):
        if line.strip():
            expected_ids.append(int(line.strip()))

    assert actual_ids == expected_ids, f"Expected IDs {expected_ids}, but got {actual_ids}"