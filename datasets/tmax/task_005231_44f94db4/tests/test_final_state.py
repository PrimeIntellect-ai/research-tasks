# test_final_state.py

import os
import json
import random
import string
import subprocess
import tempfile
import pytest

def test_video_graph_json():
    """Verify that the final JSON output matches the expected graph from the video."""
    json_path = "/home/user/video_graph.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist. Did you run the integration step?"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    expected_data = {
        "nodes": [
            {"id": "Alpha", "out_degree": 2, "targets": ["Beta", "Gamma"]},
            {"id": "Beta", "out_degree": 1, "targets": ["Delta"]},
            {"id": "Delta", "out_degree": 1, "targets": ["Alpha"]},
            {"id": "Gamma", "out_degree": 1, "targets": ["Delta"]}
        ]
    }

    assert data == expected_data, f"JSON content in {json_path} does not match the expected graph structure derived from the video."

def test_graph_builder_fuzzing():
    """Fuzz test the agent's graph builder script against the oracle implementation."""
    agent_script = "/home/user/graph_builder.sh"
    oracle_script = "/opt/oracle/graph_builder_oracle.sh"

    assert os.path.exists(agent_script), f"Agent script {agent_script} is missing."
    assert os.path.exists(oracle_script), f"Oracle script {oracle_script} is missing."

    random.seed(42)
    chars = string.ascii_letters + string.digits

    for i in range(100):
        num_lines = random.randint(0, 200)
        lines = []
        for _ in range(num_lines):
            len1 = random.randint(3, 10)
            len2 = random.randint(3, 10)
            node1 = "".join(random.choices(chars, k=len1))
            node2 = "".join(random.choices(chars, k=len2))
            lines.append(f"{node1},{node2}")

        input_text = "\n".join(lines) + ("\n" if lines else "")

        with tempfile.NamedTemporaryFile(mode='w', delete=False) as tf:
            tf.write(input_text)
            temp_path = tf.name

        try:
            agent_res = subprocess.run(["bash", agent_script, temp_path], capture_output=True, text=True)
            oracle_res = subprocess.run(["bash", oracle_script, temp_path], capture_output=True, text=True)

            # Since formatting could slightly differ even with jq, we parse the JSON to compare the actual data structure
            try:
                agent_json = json.loads(agent_res.stdout)
            except json.JSONDecodeError:
                pytest.fail(f"Agent did not output valid JSON on fuzzing iteration {i}.\nInput:\n{input_text}\nAgent Output:\n{agent_res.stdout}")

            try:
                oracle_json = json.loads(oracle_res.stdout)
            except json.JSONDecodeError:
                pytest.fail(f"Oracle did not output valid JSON on fuzzing iteration {i}.\nInput:\n{input_text}\nOracle Output:\n{oracle_res.stdout}")

            assert agent_json == oracle_json, (
                f"JSON mismatch on fuzzing iteration {i}.\n"
                f"Input:\n{input_text}\n"
                f"Agent Output:\n{json.dumps(agent_json, indent=2)}\n"
                f"Oracle Output:\n{json.dumps(oracle_json, indent=2)}"
            )
        finally:
            os.remove(temp_path)