# test_final_state.py
import os
import json
import glob
import subprocess
import pytest

def test_video_graph_json():
    json_path = "/home/user/video_graph.json"
    assert os.path.isfile(json_path), f"Missing {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not a valid JSON file.")

    assert "edges" in data, "JSON must contain 'edges' key"
    edges = data["edges"]

    expected_edges = [
        {"from": "T100", "to": "R50", "type": "HOLDS"},
        {"from": "T101", "to": "R51", "type": "HOLDS"},
        {"from": "T100", "to": "R51", "type": "WAITS_FOR"},
        {"from": "T102", "to": "R52", "type": "HOLDS"},
        {"from": "T101", "to": "R50", "type": "WAITS_FOR"}
    ]

    assert len(edges) == len(expected_edges), f"Expected {len(expected_edges)} edges, got {len(edges)}"

    for expected in expected_edges:
        assert expected in edges, f"Missing expected edge: {expected}"

def test_adversarial_corpus():
    script_py = "/home/user/detect_deadlocks.py"
    script_sh = "/home/user/detect_deadlocks.sh"

    if os.path.isfile(script_py):
        cmd_base = ["python3", script_py]
    elif os.path.isfile(script_sh):
        cmd_base = ["bash", script_sh]
    else:
        pytest.fail("Could not find detect_deadlocks.py or detect_deadlocks.sh in /home/user/")

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))
    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    for evil_file in evil_files:
        res = subprocess.run(cmd_base + [evil_file], capture_output=True, text=True)
        out = res.stdout.strip()
        if out != "DEADLOCK":
            evil_bypassed.append(os.path.basename(evil_file))

    for clean_file in clean_files:
        res = subprocess.run(cmd_base + [clean_file], capture_output=True, text=True)
        out = res.stdout.strip()
        if out != "SAFE":
            clean_modified.append(os.path.basename(clean_file))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {evil_bypassed}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {clean_modified}")

    if errors:
        pytest.fail(" | ".join(errors))