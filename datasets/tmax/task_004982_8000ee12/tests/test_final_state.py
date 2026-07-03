# test_final_state.py

import os
import json
import time
import subprocess
import pytest

def test_optimized_script_exists_and_executable():
    script_path = "/home/user/optimized.sh"
    assert os.path.isfile(script_path), f"Missing optimized script: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_result_json_correctness():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Missing result file: {result_path}"

    with open(result_path, "r") as f:
        try:
            agent_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} does not contain valid JSON.")

    expected_cmd = "jq -s '[.[] | select(.status==\"active\")] | group_by(.department) | map({department: .[0].department, total_salary: (map(.salary) | add)}) | sort_by(.total_salary) | reverse | .[0:5]' /app/data.jsonl"

    try:
        expected_out = subprocess.check_output(expected_cmd, shell=True, text=True)
        expected_json = json.loads(expected_out)
    except Exception as e:
        pytest.fail(f"Failed to compute expected JSON: {e}")

    assert agent_json == expected_json, "The output JSON does not match the expected JSON output."

def test_performance_speedup():
    baseline_script = "/app/baseline.sh"
    agent_script = "/home/user/optimized.sh"

    # Measure baseline time
    start = time.time()
    subprocess.run([baseline_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    baseline_time = time.time() - start

    # Measure agent time
    start = time.time()
    subprocess.run([agent_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    agent_time = time.time() - start

    # Prevent division by zero
    agent_time = max(agent_time, 1e-6)

    speedup = baseline_time / agent_time

    assert speedup >= 15.0, f"Speedup threshold not met. Baseline: {baseline_time:.2f}s, Agent: {agent_time:.2f}s, Speedup: {speedup:.2f}x (Threshold: 15.0x)"