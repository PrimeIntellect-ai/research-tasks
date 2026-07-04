# test_final_state.py

import os
import time
import subprocess
import pytest

def run_redis_cmd(*args):
    result = subprocess.run(["redis-cli"] + list(args), capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Redis command failed: {' '.join(args)}\n{result.stderr}")
    return result.stdout.strip()

def test_services_running():
    # Check if Nginx is listening on 8080
    nginx_check = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:8080/"], capture_output=True, text=True)
    # It might return 403 or 404 depending on config, but it shouldn't fail to connect
    assert nginx_check.returncode == 0, "Nginx is not running or not listening on port 8080"

    # Check if Redis is up
    ping_res = run_redis_cmd("PING")
    assert ping_res == "PONG", "Redis is not running or not responding to PING"

def test_worker_processing():
    clean_dir = "/app/data/clean"
    evil_dir = "/app/data/evil"

    assert os.path.exists(clean_dir), f"Clean corpus directory missing: {clean_dir}"
    assert os.path.exists(evil_dir), f"Evil corpus directory missing: {evil_dir}"

    clean_files = [f"clean/{f}" for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [f"evil/{f}" for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    total_files = len(clean_files) + len(evil_files)
    assert total_files > 0, "No corpus files found to process."

    # Clear queues
    run_redis_cmd("DEL", "processing_tasks", "processing_results")

    # Push tasks
    all_tasks = clean_files + evil_files
    for task in all_tasks:
        run_redis_cmd("RPUSH", "processing_tasks", task)

    # Wait for processing
    timeout = 15
    start_time = time.time()
    while time.time() - start_time < timeout:
        llen_out = run_redis_cmd("LLEN", "processing_results")
        if llen_out.isdigit() and int(llen_out) == total_files:
            break
        time.sleep(0.5)

    # Fetch results
    results_out = run_redis_cmd("LRANGE", "processing_results", "0", "-1")
    results = results_out.split("\n") if results_out else []

    # Parse results
    result_map = {}
    for res in results:
        if not res:
            continue
        parts = res.split(":", 1)
        if len(parts) == 2:
            result_map[parts[0]] = parts[1]

    # Verify clean corpus
    clean_failed = []
    for cf in clean_files:
        if result_map.get(cf) != "CLEAN":
            clean_failed.append(cf)

    # Verify evil corpus
    evil_failed = []
    for ef in evil_files:
        if result_map.get(ef) != "EVIL":
            evil_failed.append(ef)

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed[:5])}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed[:5])}")

    missing = total_files - len(result_map)
    if missing > 0:
        error_msgs.append(f"{missing} files were not processed at all (missing from results).")

    assert not error_msgs, " | ".join(error_msgs)