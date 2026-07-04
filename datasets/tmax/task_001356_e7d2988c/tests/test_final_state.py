# test_final_state.py
import os
import time
import subprocess
import pytest

def test_redis_dbsize_metric():
    """
    Evaluates the final state of the system by restarting services,
    blasting the UDP packets, and checking the number of processed
    payloads in Redis.
    """
    # 1. Terminate any existing background processes to ensure a clean state
    subprocess.run(["pkill", "-f", "collector.py"], capture_output=True)
    subprocess.run(["pkill", "-f", "redis-server"], capture_output=True)
    time.sleep(1)

    # 2. Run /app/start_services.sh
    subprocess.Popen(
        ["/app/start_services.sh"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        preexec_fn=os.setsid
    )

    # 3. Wait 2 seconds for services to fully initialize
    time.sleep(2)

    # Ensure Redis is empty before we start the simulation
    subprocess.run(["redis-cli", "FLUSHALL"], capture_output=True)

    # 4. Run /app/run_malware.sh
    subprocess.run(["/app/run_malware.sh"], capture_output=True)

    # 5. Wait 3 seconds for the collector to process the UDP queue
    time.sleep(3)

    # 6. Query redis-cli DBSIZE
    result = subprocess.run(["redis-cli", "DBSIZE"], capture_output=True, text=True)

    try:
        dbsize = int(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Could not parse redis-cli DBSIZE output. Raw output: {result.stdout}")

    # The target value is 10000, threshold >= 9500
    assert dbsize >= 9500, (
        f"Metric threshold failed: Expected DBSIZE >= 9500, but got {dbsize}. "
        "The recursion and concurrency bugs in collector.py likely still limit throughput."
    )

def test_debugging_summary_exists():
    """
    Checks if the debugging summary log file was created at the specified path.
    """
    path = "/home/user/debugging_summary.txt"
    assert os.path.isfile(path), f"Debugging summary log file is missing at {path}"