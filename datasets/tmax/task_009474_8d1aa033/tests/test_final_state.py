# test_final_state.py

import os
import json
import pytest

def test_script_exists():
    script_path = "/home/user/analyze_graph.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_output_json_exists_and_correct():
    output_path = "/home/user/influence_metrics.json"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} does not contain valid JSON.")

    assert "seed_paper" in data, "The key 'seed_paper' is missing from the output JSON."
    assert data["seed_paper"] == "P001", f"Expected 'seed_paper' to be 'P001', but got {data['seed_paper']}."

    assert "author_name" in data, "The key 'author_name' is missing from the output JSON."
    assert data["author_name"] == "Dr. Alice", f"Expected 'author_name' to be 'Dr. Alice', but got {data['author_name']}."

    assert "total_citing_papers" in data, "The key 'total_citing_papers' is missing from the output JSON."
    assert data["total_citing_papers"] == 4, f"Expected 'total_citing_papers' to be 4, but got {data['total_citing_papers']}."

    assert "total_influence_score" in data, "The key 'total_influence_score' is missing from the output JSON."
    assert float(data["total_influence_score"]) == 11.0, f"Expected 'total_influence_score' to be 11.0, but got {data['total_influence_score']}."