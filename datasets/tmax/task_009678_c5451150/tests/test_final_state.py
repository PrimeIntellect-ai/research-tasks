# test_final_state.py
import os
import json
import pytest
import stat

def test_init_graph_script_exists():
    assert os.path.isfile("/home/user/init_graph.py"), "/home/user/init_graph.py is missing."

def test_kuzu_db_directory_exists():
    assert os.path.isdir("/home/user/kuzu_db"), "/home/user/kuzu_db directory is missing. Did the init script run?"

def test_query_cypher_exists():
    assert os.path.isfile("/home/user/query.cypher"), "/home/user/query.cypher is missing."

def test_bash_script_exists_and_executable():
    script_path = "/home/user/execute_and_validate.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_output_json_correctness():
    output_path = "/home/user/output.json"
    assert os.path.isfile(output_path), f"{output_path} is missing. Did the bash script run successfully?"

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} does not contain valid JSON.")

    expected_data = [
        {"target_name": "Eve", "total_weight": 1.7},
        {"target_name": "Frank", "total_weight": 1.7},
        {"target_name": "Diana", "total_weight": 1.3}
    ]

    assert isinstance(data, list), "Output JSON must be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} results, got {len(data)}."

    for i, expected in enumerate(expected_data):
        assert data[i].get("target_name") == expected["target_name"], f"Result {i} target_name mismatch. Expected {expected['target_name']}, got {data[i].get('target_name')}"
        # using pytest.approx for floating point comparison
        assert data[i].get("total_weight") == pytest.approx(expected["total_weight"], rel=1e-5), f"Result {i} total_weight mismatch. Expected {expected['total_weight']}, got {data[i].get('total_weight')}"