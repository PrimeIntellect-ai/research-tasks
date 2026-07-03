# test_final_state.py

import os
import pytest

def test_alice_collaborators():
    """Test that alice_collaborators.txt contains the correct direct collaborators."""
    file_path = '/home/user/alice_collaborators.txt'
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content, f"File {file_path} is empty."

    collabs = [x.strip() for x in content.split(',')]
    assert set(collabs) == {"Dr. Bob", "Dr. Charlie"}, \
        f"Expected collaborators 'Dr. Bob' and 'Dr. Charlie', but got {collabs}"

def test_shortest_path():
    """Test that shortest_path.txt contains a valid shortest path."""
    file_path = '/home/user/shortest_path.txt'
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        path = f.read().strip()

    valid_paths = [
        "Dr. Alice,Dr. Bob,Dr. Delta,Dr. Zeta",
        "Dr. Alice,Dr. Charlie,Dr. Echo,Dr. Zeta"
    ]

    assert path in valid_paths, \
        f"Shortest path '{path}' is not one of the valid shortest paths: {valid_paths}"

def test_query_plan():
    """Test that query_plan.txt contains typical SPARQL algebra representation."""
    file_path = '/home/user/query_plan.txt'
    assert os.path.exists(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        plan = f.read().strip()

    assert len(plan) > 10, f"File {file_path} content is too short to be a valid query plan."
    assert "BGP" in plan or "Project" in plan, \
        f"File {file_path} does not seem to contain a typical rdflib SPARQL algebra representation (missing 'BGP' or 'Project')."