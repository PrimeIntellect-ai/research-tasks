# test_final_state.py
import json
import os
import urllib.request
import ast

def test_final_config_json_accuracy():
    config_path = '/app/final_config.json'
    assert os.path.isfile(config_path), f"File {config_path} does not exist."

    with open(config_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{config_path} is not valid JSON."

    assert isinstance(data, list), f"Expected JSON array in {config_path}, got {type(data)}."

    ground_truth = [
        {"module": "Auth", "version": "1.2.4"},
        {"module": "Data", "version": "2.0.1"},
        {"module": "Sink", "version": "0.9.4"}
    ]

    matches = 0
    for i in range(min(len(data), len(ground_truth))):
        if isinstance(data[i], dict):
            if data[i].get("module", "").lower() == ground_truth[i]["module"].lower() and \
               data[i].get("version", "") == ground_truth[i]["version"]:
                matches += 1

    accuracy = matches / len(ground_truth)
    assert accuracy >= 1.0, f"Accuracy of extracted data is {accuracy}, expected >= 1.0. Got: {data}"

def test_server_running_and_config():
    try:
        req = urllib.request.Request("http://localhost:8080/config")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        assert False, f"Failed to fetch /config from server on port 8080: {e}"

    assert isinstance(data, list), f"Expected JSON array from server, got {type(data)}."

    ground_truth = [
        {"module": "Auth", "version": "1.2.4"},
        {"module": "Data", "version": "2.0.1"},
        {"module": "Sink", "version": "0.9.4"}
    ]

    matches = 0
    for i in range(min(len(data), len(ground_truth))):
        if isinstance(data[i], dict):
            if data[i].get("module", "").lower() == ground_truth[i]["module"].lower() and \
               data[i].get("version", "") == ground_truth[i]["version"]:
                matches += 1

    accuracy = matches / len(ground_truth)
    assert accuracy >= 1.0, f"Accuracy of server /config data is {accuracy}, expected >= 1.0. Got: {data}"

def test_python3_syntax():
    script_path = '/app/legacy_processor.py'
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    with open(script_path, 'r') as f:
        source = f.read()

    try:
        ast.parse(source)
    except SyntaxError as e:
        assert False, f"{script_path} is not valid Python 3 syntax: {e}"