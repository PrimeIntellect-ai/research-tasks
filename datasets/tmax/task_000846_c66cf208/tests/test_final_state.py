# test_final_state.py

import os
import requests
import pytest

def test_graph_materialized():
    """Check if the RDF graph was materialized to the correct file."""
    assert os.path.exists('/home/user/data/graph.ttl'), "Graph file /home/user/data/graph.ttl does not exist. Did you run the graph materialization script?"

def test_service_status_log():
    """Check if the service status log exists and indicates readiness."""
    log_path = '/home/user/service_status.log'
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."
    with open(log_path, 'r') as f:
        content = f.read()
        assert "SERVICES READY" in content, f"Log file does not contain 'SERVICES READY'. Content: {content}"

def test_nginx_auth_required():
    """Verify that the Nginx gateway requires authentication."""
    try:
        response = requests.get('http://127.0.0.1:8080/shortest-path?start=Alpha&end=Delta', timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to Nginx on 127.0.0.1:8080. Is it running?")

    assert response.status_code == 401, f"Expected 401 Unauthorized without auth, got {response.status_code}."

def test_shortest_path_endpoint():
    """Verify the shortest path calculation for Alpha to Delta."""
    auth = ('analyst', 'graph123')
    try:
        response = requests.get('http://127.0.0.1:8080/shortest-path?start=Alpha&end=Delta', auth=auth, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to Nginx on 127.0.0.1:8080. Is it running?")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    assert "path" in data, "Response JSON is missing the 'path' key."
    assert "total_cost" in data, "Response JSON is missing the 'total_cost' key."

    expected_path = ["Alpha", "Beta", "Gamma", "Delta"]
    expected_cost = 35

    assert data["path"] == expected_path, f"Expected path {expected_path}, but got {data['path']}."
    assert data["total_cost"] == expected_cost, f"Expected total_cost {expected_cost}, but got {data['total_cost']}."

def test_sparql_endpoint():
    """Verify the SPARQL endpoint executes queries correctly."""
    auth = ('analyst', 'graph123')
    query = """
    PREFIX log: <http://example.org/logistics/>
    SELECT ?s ?o WHERE {
        ?s log:connectedTo ?o .
    }
    """
    try:
        response = requests.post('http://127.0.0.1:8080/sparql', json={"query": query}, auth=auth, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to Nginx on 127.0.0.1:8080. Is it running?")

    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {response.text}")

    # Verify it looks like a SPARQL JSON results format
    assert isinstance(data, dict), "SPARQL response should be a JSON object."
    assert "head" in data or "results" in data or "boolean" in data, "Response does not match standard SPARQL JSON format."