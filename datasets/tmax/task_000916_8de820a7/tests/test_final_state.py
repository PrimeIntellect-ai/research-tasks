# test_final_state.py

import os
import json
import random
import subprocess
import requests
import pytest

def test_best_pipeline_exists():
    assert os.path.exists("/home/user/best_pipeline.pkl"), "The best_pipeline.pkl file was not found."
    assert os.path.isfile("/home/user/best_pipeline.pkl"), "/home/user/best_pipeline.pkl is not a file."

def test_api_and_model_correctness():
    # Generate a random 1024-D vector
    random.seed(42)
    vector = [random.uniform(-1.0, 1.0) for _ in range(1024)]

    # 1. Test API response
    url = "http://127.0.0.1:8080/score"
    payload = {"raw_embedding": vector}

    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the API at {url}: {e}")

    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"API did not return valid JSON. Response: {response.text}")

    assert "class" in data, "Response JSON is missing 'class' key."
    assert "inference_time_ms" in data, "Response JSON is missing 'inference_time_ms' key."

    api_class = data["class"]
    assert api_class in [0, 1], f"Expected 'class' to be 0 or 1, got {api_class}"

    inference_time = data["inference_time_ms"]
    assert isinstance(inference_time, (int, float)) and inference_time > 0, f"Expected 'inference_time_ms' to be a positive number, got {inference_time}"

    # 2. Test against the saved pipeline
    # We use the student's environment to load the model and predict
    env_python = "/home/user/env/bin/python"
    assert os.path.exists(env_python), f"Student's python environment not found at {env_python}"

    script = """
import sys
import pickle
import json

try:
    with open('/home/user/best_pipeline.pkl', 'rb') as f:
        model = pickle.load(f)
    vector = json.loads(sys.argv[1])
    pred = model.predict([vector])[0]
    print(int(pred))
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
"""

    script_path = "/tmp/verify_model.py"
    with open(script_path, "w") as f:
        f.write(script)

    result = subprocess.run(
        [env_python, script_path, json.dumps(vector)],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Failed to run model prediction using saved pipeline. Error: {result.stdout}\n{result.stderr}"

    try:
        model_class = int(result.stdout.strip())
    except ValueError:
        pytest.fail(f"Unexpected output from model script: {result.stdout}")

    assert api_class == model_class, f"API returned class {api_class}, but the saved pipeline predicted class {model_class} for the same input."