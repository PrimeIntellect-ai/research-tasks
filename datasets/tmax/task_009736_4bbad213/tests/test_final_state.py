# test_final_state.py
import os
import json

def test_path_analysis_json():
    json_path = "/home/user/path_analysis.json"
    assert os.path.isfile(json_path), f"The file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {json_path} contains invalid JSON."

    expected = [
      {"paper": "http://example.org/paper/P1", "author_total_papers": 2},
      {"paper": "http://example.org/paper/P3", "author_total_papers": 1},
      {"paper": "http://example.org/paper/P6", "author_total_papers": 4},
      {"paper": "http://example.org/paper/P8", "author_total_papers": 3}
    ]

    assert data == expected, f"Content of {json_path} is incorrect. Expected {expected}, got {data}"

def test_original_file_unmodified():
    nt_file_path = "/home/user/citation_graph.nt"
    assert os.path.isfile(nt_file_path), f"The original dataset file {nt_file_path} is missing."

    with open(nt_file_path, "r") as f:
        content = f.read()

    expected_lines = [
        "<http://example.org/paper/P1> <http://example.org/ontology/cites> <http://example.org/paper/P2> .",
        "<http://example.org/paper/P1> <http://example.org/ontology/cites> <http://example.org/paper/P3> .",
        "<http://example.org/paper/P8> <http://example.org/ontology/cites> <http://example.org/paper/P9> .",
        "<http://example.org/paper/P1> <http://example.org/ontology/authoredBy> <http://example.org/author/A1> .",
        "<http://example.org/paper/P10> <http://example.org/ontology/authoredBy> <http://example.org/author/A4> ."
    ]

    for line in expected_lines:
        assert line in content, f"Original file {nt_file_path} was modified. Missing line: '{line}'"