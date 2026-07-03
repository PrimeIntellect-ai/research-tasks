# test_final_state.py

import os
import ast
import json
import urllib.request
import urllib.error
import pytest

def test_bench_result_exists_and_valid():
    """Check if /home/user/bench_result.txt exists and contains a valid float number."""
    filepath = "/home/user/bench_result.txt"
    assert os.path.exists(filepath), f"File {filepath} does not exist."
    assert os.path.isfile(filepath), f"{filepath} is not a file."

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content, f"File {filepath} is empty."

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {filepath} is not a valid float: {content}")

    assert val > 0, "Benchmark time should be greater than 0."

def test_api_projects_endpoint():
    """Check GET /projects returns the correct list of project names."""
    url = "http://localhost:8000/projects"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    expected = ["FrontendClient", "PaymentGateway", "DataPipeline"]
    # Order might not be strictly guaranteed depending on dict iteration, but usually is.
    # We will check if the sets match.
    assert isinstance(data, list), "Expected a JSON list response."
    assert set(data) == set(expected), f"Expected projects {expected}, got {data}"

def test_api_actions_endpoint_success():
    """Check GET /actions/PaymentGateway returns the correct actions and files."""
    url = "http://localhost:8000/actions/PaymentGateway"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

    expected = [
        {"action": "refactor", "file": "app/services/stripe.py"},
        {"action": "secure", "file": "app/config/keys.py"},
        {"action": "test", "file": "tests/integration/test_stripe.py"}
    ]
    assert data == expected, f"Expected {expected}, got {data}"

def test_api_actions_endpoint_not_found():
    """Check GET /actions/UnknownProject returns 404."""
    url = "http://localhost:8000/actions/UnknownProject"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            pytest.fail("Expected 404 Not Found, but got 200 OK.")
    except urllib.error.HTTPError as e:
        assert e.code == 404, f"Expected status 404, got {e.code}"
        data = json.loads(e.read().decode("utf-8"))
        assert data.get("detail") == "Project not found", f"Expected 'Project not found' detail, got {data}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to API at {url}: {e}")

def test_parser_implementation():
    """Inspect /home/user/parser.py to ensure it uses a state-machine approach and contains ActLogParser."""
    filepath = "/home/user/parser.py"
    assert os.path.exists(filepath), f"File {filepath} does not exist."

    with open(filepath, "r") as f:
        source = f.read()

    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        pytest.fail(f"Syntax error in {filepath}: {e}")

    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    assert "ActLogParser" in classes, "Class ActLogParser not found in parser.py"

    assert "re." not in source and "import re" not in source, "Regular expressions (re module) should not be used."