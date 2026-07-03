# test_final_state.py

import os
import subprocess
import time
import pytest

def test_files_exist():
    submit_py = "/home/user/submit_telemetry.py"
    run_all_sh = "/home/user/run_all.sh"

    assert os.path.isfile(submit_py), f"Missing Python script: {submit_py}"
    assert os.path.isfile(run_all_sh), f"Missing bash script: {run_all_sh}"

def test_nginx_proxy_configured():
    # Check if Nginx is listening on 8080
    res = subprocess.run(["curl", "-I", "http://localhost:8080/"], capture_output=True, text=True)
    # Even if it returns 404, it should be served by nginx/flask
    assert "nginx" in res.stdout.lower() or "gunicorn" in res.stdout.lower() or "werkzeug" in res.stdout.lower() or res.returncode == 0, "Nginx is not proxying port 8080 properly."

def test_execution_time_and_redis_state():
    # Flush Redis to ensure a clean state
    subprocess.run(["redis-cli", "FLUSHALL"], check=True)

    # Run the submission script and measure time
    start_time = time.time()
    res = subprocess.run(["python3", "/home/user/submit_telemetry.py"], capture_output=True, text=True)
    end_time = time.time()

    duration = end_time - start_time

    assert res.returncode == 0, f"submit_telemetry.py failed with error: {res.stderr}"
    assert duration <= 2.5, f"Execution time {duration:.3f} seconds exceeds the threshold of 2.5 seconds."

    # Query Redis to ensure records were inserted
    # Since the exact key or structure isn't specified, we can check memory or keyspace
    # If the API stores each as a key, dbsize will be 50000. If stored in a list/set, dbsize is >= 1.
    dbsize_res = subprocess.run(["redis-cli", "DBSIZE"], capture_output=True, text=True)
    dbsize = int(dbsize_res.stdout.strip())

    # If stored as individual keys
    if dbsize == 50000:
        pass
    else:
        # If stored in a list or set, check if there's any key with 50000 elements
        keys_res = subprocess.run(["redis-cli", "KEYS", "*"], capture_output=True, text=True)
        keys = keys_res.stdout.strip().split()

        found_50k = False
        for key in keys:
            type_res = subprocess.run(["redis-cli", "TYPE", key], capture_output=True, text=True)
            ktype = type_res.stdout.strip()

            if ktype == "list":
                len_res = subprocess.run(["redis-cli", "LLEN", key], capture_output=True, text=True)
                if int(len_res.stdout.strip()) == 50000:
                    found_50k = True
                    break
            elif ktype == "set":
                len_res = subprocess.run(["redis-cli", "SCARD", key], capture_output=True, text=True)
                if int(len_res.stdout.strip()) == 50000:
                    found_50k = True
                    break

        assert found_50k or dbsize == 50000, "Could not find exactly 50,000 records inserted into Redis."