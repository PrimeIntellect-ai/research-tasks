# test_final_state.py

import os
import sys
import time
import requests
import subprocess
import pytest

def test_api_accuracy():
    app_path = "/home/user/app.py"
    assert os.path.exists(app_path), f"FastAPI app {app_path} does not exist."

    # Start the FastAPI server in the background
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--port", "8000"],
        cwd="/home/user",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        # Wait for the server to start
        time.sleep(3)

        score = 0
        total = 5

        # Test 1: Basic Math & Pixel reading
        script1 = "SEEK 10\nLUM 50 50 R1\nRET R1"
        try:
            r1 = requests.post("http://localhost:8000/execute", json={"script": script1, "client_id": "client1"}, timeout=5)
            if r1.status_code == 200 and isinstance(r1.json().get("result"), int):
                score += 1
        except Exception:
            pass

        # Test 2: Rate Limit 1
        try:
            requests.post("http://localhost:8000/execute", json={"script": script1, "client_id": "client1"}, timeout=5)
            requests.post("http://localhost:8000/execute", json={"script": script1, "client_id": "client1"}, timeout=5)
            r2 = requests.post("http://localhost:8000/execute", json={"script": script1, "client_id": "client1"}, timeout=5)
            if r2.status_code == 429:
                score += 1
        except Exception:
            pass

        # Test 3: Validation
        try:
            r3 = requests.post("http://localhost:8000/execute", json={"script": "INVALID COMMAND", "client_id": "client2"}, timeout=5)
            if r3.status_code == 400:
                score += 1
        except Exception:
            pass

        # Test 4: Logic / Loops
        script2 = "SEEK 0\nLUM 10 10 R0\nADD R1 R0\nRET R1"
        try:
            r4 = requests.post("http://localhost:8000/execute", json={"script": script2, "client_id": "client3"}, timeout=5)
            if r4.status_code == 200 and isinstance(r4.json().get("result"), int):
                score += 1
        except Exception:
            pass

        # Test 5: Rate limit regeneration
        try:
            time.sleep(21)
            r5 = requests.post("http://localhost:8000/execute", json={"script": script1, "client_id": "client1"}, timeout=5)
            if r5.status_code == 200:
                score += 1
        except Exception:
            pass

        accuracy = score / total
        assert accuracy >= 1.0, f"API Accuracy Score: {accuracy} < 1.0 (Target: 1.0)"

    finally:
        process.terminate()
        process.wait(timeout=5)