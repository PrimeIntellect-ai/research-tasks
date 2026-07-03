# test_final_state.py

import os
import json
import pytest

def test_output_json_exists_and_correct():
    """Check if output.json exists, is valid JSON, and contains the correct results."""
    output_file = "/home/user/output.json"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist. The Rust program must create this file."

    with open(output_file, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {output_file} is not valid JSON.")

    assert "highest_degree_name" in data, "Missing 'highest_degree_name' key in JSON output."
    assert "total_edges" in data, "Missing 'total_edges' key in JSON output."
    assert "total_triangles" in data, "Missing 'total_triangles' key in JSON output."

    expected_name = "Charlie"
    expected_edges = 8
    expected_triangles = 3

    assert data["highest_degree_name"] == expected_name, f"Expected highest_degree_name to be '{expected_name}', got '{data['highest_degree_name']}'."
    assert data["total_edges"] == expected_edges, f"Expected total_edges to be {expected_edges}, got {data['total_edges']}."
    assert data["total_triangles"] == expected_triangles, f"Expected total_triangles to be {expected_triangles}, got {data['total_triangles']}."