# test_final_state.py

import os
import time
import json
import subprocess
import pytest

def test_fast_graph_exists():
    assert os.path.isfile("/home/user/fast_graph.c"), "The source file /home/user/fast_graph.c does not exist."
    assert os.path.isfile("/home/user/fast_graph"), "The compiled binary /home/user/fast_graph does not exist."
    assert os.access("/home/user/fast_graph", os.X_OK), "The binary /home/user/fast_graph is not executable."

def measure(cmd):
    start = time.time()
    res = subprocess.run(cmd, capture_output=True, text=True)
    duration = time.time() - start
    return duration, res.stdout, res.returncode

def test_speedup_and_correctness():
    csv_path = "/home/user/data/network_logs.csv"
    assert os.path.isfile(csv_path), f"{csv_path} does not exist."

    ref_cmd = ["/app/path_finder", csv_path, "A100", "Z999"]
    agent_cmd = ["/home/user/fast_graph", csv_path, "A100", "Z999"]

    ref_time, ref_out, ref_rc = measure(ref_cmd)
    assert ref_rc == 0, f"Reference binary failed with return code {ref_rc}"

    agent_time, agent_out, agent_rc = measure(agent_cmd)
    assert agent_rc == 0, f"Agent binary failed with return code {agent_rc}"

    result_json_path = "/home/user/result.json"
    assert os.path.isfile(result_json_path), f"The result file {result_json_path} was not created."

    try:
        ref_json = json.loads(ref_out)
    except json.JSONDecodeError:
        pytest.fail("Reference binary did not output valid JSON.")

    try:
        with open(result_json_path, "r") as f:
            agent_json = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"Agent output file {result_json_path} does not contain valid JSON.")

    assert "path" in ref_json, "Reference JSON missing 'path' key."
    assert "path" in agent_json, "Agent JSON missing 'path' key."

    assert ref_json["path"] == agent_json["path"], f"Paths do not match. Expected {ref_json['path']}, got {agent_json['path']}."

    assert "hops" in agent_json, "Agent JSON missing 'hops' key."
    assert "bottleneck_capacity" in agent_json, "Agent JSON missing 'bottleneck_capacity' key."

    if agent_time == 0:
        agent_time = 1e-9  # Prevent division by zero

    speedup = ref_time / agent_time
    assert speedup >= 10.0, f"Speedup {speedup:.2f}x is below the 10.0x threshold. (Ref: {ref_time:.4f}s, Agent: {agent_time:.4f}s)"