# test_final_state.py

import os
import subprocess
import random
import time
import json
import urllib.request
import urllib.error
import pytest

def test_fuzz_equivalence():
    oracle_path = "/app/oracle"
    agent_script = "/home/user/fixed_math.py"

    assert os.path.isfile(oracle_path), f"Oracle missing at {oracle_path}"
    assert os.path.isfile(agent_script), f"Agent script missing at {agent_script}"

    random.seed(42)
    inputs = [random.randint(0, 100000) for _ in range(100)]

    for val in inputs:
        oracle_res = subprocess.run([oracle_path, str(val)], capture_output=True, text=True)
        agent_res = subprocess.run(["python3", agent_script, str(val)], capture_output=True, text=True)

        assert oracle_res.returncode == 0, f"Oracle failed on input {val}"
        assert agent_res.returncode == 0, f"Agent script failed on input {val}\nstderr: {agent_res.stderr}"

        oracle_out = oracle_res.stdout.strip()
        agent_out = agent_res.stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on input {val}: oracle={oracle_out}, agent={agent_out}"

def test_end_to_end_api():
    # Start the services
    start_sh_path = "/app/start.sh"
    assert os.path.isfile(start_sh_path), f"Startup script missing at {start_sh_path}"

    # Clean up any existing services first
    subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True)
    subprocess.run(["pkill", "-f", "worker.py"], capture_output=True)
    subprocess.run(["pkill", "-f", "redis-server"], capture_output=True)
    time.sleep(1)

    process = subprocess.Popen(["/bin/bash", start_sh_path])
    time.sleep(3) # Wait for services to initialize

    try:
        random.seed(1337)
        inputs = [random.randint(0, 1000) for _ in range(5)]

        for val in inputs:
            oracle_res = subprocess.run(["/app/oracle", str(val)], capture_output=True, text=True)
            expected_out = int(oracle_res.stdout.strip())

            req = urllib.request.Request(
                "http://127.0.0.1:8000/compute",
                data=json.dumps({"value": val}).encode("utf-8"),
                headers={"Content-Type": "application/json"}
            )

            try:
                with urllib.request.urlopen(req) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
            except urllib.error.URLError as e:
                pytest.fail(f"API request failed for input {val}. Is the service running properly? Error: {e}")

            assert "result" in res_data, f"API response missing 'result' key: {res_data}"
            assert res_data["result"] == expected_out, f"API returned wrong result for {val}: expected {expected_out}, got {res_data['result']}"

    finally:
        # Cleanup
        subprocess.run(["pkill", "-f", "uvicorn"], capture_output=True)
        subprocess.run(["pkill", "-f", "worker.py"], capture_output=True)
        subprocess.run(["pkill", "-f", "redis-server"], capture_output=True)