# test_final_state.py
import os
import json
import pytest

def test_resolution_log_exists():
    """Test that resolution.log exists."""
    assert os.path.isfile('/home/user/ticket_8992/resolution.log'), "The file /home/user/ticket_8992/resolution.log is missing."

def test_resolution_log_content():
    """Test that resolution.log contains the correct IP and an integer iteration count."""
    with open('/home/user/ticket_8992/resolution.log', 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, "resolution.log must contain at least two lines."
    assert lines[0] == "10.99.99.99", f"Line 1 of resolution.log should be '10.99.99.99', but got '{lines[0]}'."

    try:
        iterations = int(lines[1])
    except ValueError:
        pytest.fail(f"Line 2 of resolution.log must be an integer iteration count, but got '{lines[1]}'.")

    assert iterations > 0, "Iteration count should be greater than 0."

def test_topology_json_exists_and_valid():
    """Test that topology.json exists and contains valid JSON data."""
    assert os.path.isfile('/home/user/ticket_8992/topology.json'), "The file /home/user/ticket_8992/topology.json is missing. Did you run the fixed script?"

    with open('/home/user/ticket_8992/topology.json', 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("topology.json does not contain valid JSON.")

    assert isinstance(data, dict), "topology.json should contain a JSON object (dictionary) of nodes."
    assert "10.99.99.99" in data, "The anomalous IP '10.99.99.99' should be present in the topology.json output."

    # Check that convergence happened and weights are present
    for ip, node_data in data.items():
        assert 'weight' in node_data, f"Node {ip} is missing a 'weight' value in topology.json."
        assert isinstance(node_data['weight'], (int, float)), f"Node {ip} weight is not a number."