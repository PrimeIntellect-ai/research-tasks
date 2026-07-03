# test_final_state.py

import os
import json
import math
import requests
import pytest

def test_parser_bug_fixed():
    path = "/app/vendored/pylogcalc-0.1.0/pylogcalc/parser.py"
    assert os.path.isfile(path), f"File missing: {path}"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "msg.encode('ascii')" not in content, "The bug (forcing ascii encoding) is still present in parser.py"
    assert "msg.encode('utf-8')" in content or 'msg.encode("utf-8")' in content or "msg.encode('utf8')" in content or 'msg.encode("utf8")' in content, "The encoding was not changed to utf-8 in parser.py"

def test_api_endpoint_returns_correct_data():
    # Derive expected data
    logs_path = "/home/user/logs.jsonl"
    assert os.path.isfile(logs_path), f"File missing: {logs_path}"

    logs = []
    with open(logs_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                logs.append(json.loads(line))

    # Stratified sampling
    lang_counts = {}
    sampled_logs = []
    for log in sorted(logs, key=lambda x: x["id"]):
        lang = log["lang"]
        if lang_counts.get(lang, 0) < 5:
            sampled_logs.append(log)
            lang_counts[lang] = lang_counts.get(lang, 0) + 1

    # Calculate risk
    def calc_risk(log):
        dist = math.sqrt(log["x"]**2 + log["y"]**2)
        msg_len = len(log["message"].encode("utf-8"))
        return dist + msg_len * 0.1

    for log in sampled_logs:
        log["risk"] = calc_risk(log)

    # Sort by risk desc, id asc
    sampled_logs.sort(key=lambda x: (-x["risk"], x["id"]))

    # Top 3
    top_3 = sampled_logs[:3]

    expected_top_anomalies = []
    for i, log in enumerate(top_3):
        expected_top_anomalies.append({
            "rank": i + 1,
            "id": log["id"],
            "risk": round(log["risk"], 2)
        })

    expected_response = {
        "status": "success",
        "top_anomalies": expected_top_anomalies
    }

    # Query the API
    try:
        response = requests.get("http://127.0.0.1:9000/api/anomalies", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP API at 127.0.0.1:9000/api/anomalies: {e}")

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type: application/json"

    try:
        actual_response = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert actual_response == expected_response, f"API response {actual_response} does not match expected {expected_response}"