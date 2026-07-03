# test_final_state.py

import os
import json
import pytest

def test_page2_json_exists_and_content():
    """Test that page2.json exists and contains the correct paginated data."""
    file_path = '/home/user/page2.json'
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did the C program run successfully?"

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    expected_data = [
        {"id": 8, "source": "MIA", "dest": "LAX", "delay": 60},
        {"id": 10, "source": "LAX", "dest": "JFK", "delay": 50},
        {"id": 4, "source": "LAX", "dest": "ORD", "delay": 45}
    ]

    assert isinstance(data, list), f"{file_path} must contain a JSON array."
    assert len(data) == len(expected_data), f"{file_path} should contain exactly {len(expected_data)} records."

    for i, expected_record in enumerate(expected_data):
        assert data[i] == expected_record, f"Record at index {i} in {file_path} does not match expected output."

def test_graph_edges_csv_exists_and_content():
    """Test that graph_edges.csv exists and contains the correct delayed SkyCorp flights."""
    file_path = '/home/user/graph_edges.csv'
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did the C program run successfully?"

    expected_lines = [
        "source,dest,weight",
        "SFO,JFK,120",
        "ATL,ORD,90",
        "SFO,LAX,80",
        "MIA,LAX,60",
        "LAX,JFK,50",
        "LAX,ORD,45",
        "ORD,JFK,35",
        "JFK,MIA,25",
        "JFK,LAX,15",
        "JFK,ATL,10",
        "ATL,JFK,5"
    ]

    with open(file_path, 'r') as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"{file_path} should have exactly {len(expected_lines)} lines."

    for i, expected_line in enumerate(expected_lines):
        assert content[i].strip() == expected_line, f"Line {i+1} in {file_path} does not match expected output."