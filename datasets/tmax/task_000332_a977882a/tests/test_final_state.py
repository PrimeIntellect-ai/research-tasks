# test_final_state.py

import os
import time
import subprocess
import redis
import shutil

def test_processor_performance_and_correctness():
    # Setup clean state
    processed_dir = "/home/user/docs_processed"
    if os.path.exists(processed_dir):
        shutil.rmtree(processed_dir)
    os.makedirs(processed_dir, exist_ok=True)

    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.flushall()
    except redis.ConnectionError:
        # If redis is not running, try to start services
        subprocess.run(["bash", "/app/start_services.sh"], check=True)
        time.sleep(2) # Give services a moment to start
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.flushall()

    # Run the processor script and measure execution time
    t0 = time.time()
    proc = subprocess.run(["python", "/app/processor.py"], capture_output=True, text=True)
    t1 = time.time()
    runtime = t1 - t0

    assert proc.returncode == 0, f"Processor script failed with return code {proc.returncode}.\nStdout: {proc.stdout}\nStderr: {proc.stderr}"

    # Verify execution time
    threshold = 3.5
    assert runtime <= threshold, f"Execution too slow: {runtime:.2f}s (Threshold: {threshold}s)"

    # Verify Redis keys
    keys = r.keys('*')
    assert len(keys) == 10000, f"Expected 10000 metrics in Redis, found {len(keys)}"

    # Verify processed directory
    processed_files = os.listdir(processed_dir)
    assert len(processed_files) == 10000, f"Expected 10000 processed files, found {len(processed_files)}."

    # Verify atomic writes by checking that no temporary files are left
    # (e.g., files starting with a dot or containing 'tmp' if any, though the count is exactly 10000)
    # We will just ensure all files end with .md
    md_files = [f for f in processed_files if f.endswith('.md')]
    assert len(md_files) == 10000, f"Expected 10000 .md files in processed directory, found {len(md_files)}."