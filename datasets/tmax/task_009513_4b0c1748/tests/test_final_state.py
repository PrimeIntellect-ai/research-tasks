# test_final_state.py
import os
import json
import pytest

def test_test_main_unmodified():
    test_main_path = "/home/user/app/test_main.py"
    assert os.path.isfile(test_main_path), "test_main.py is missing."

    expected_content = """from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_item():
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42, "name": "Item 42", "is_offer": None}

def test_create_item():
    response = client.post("/items/", json={"name": "Screwdriver", "price": 12.5})
    assert response.status_code == 200
    assert response.json() == {"name": "Screwdriver", "price": 12.5, "tax": 1.25}

def test_create_item_no_tax():
    response = client.post("/items/", json={"name": "Hammer", "price": 10.0, "tax": 0.0})
    assert response.status_code == 200
    assert response.json() == {"name": "Hammer", "price": 10.0, "tax": 0.0}"""

    with open(test_main_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), "test_main.py was modified, which is not allowed."

def test_json_report():
    report_path = "/home/user/test_report.json"
    assert os.path.isfile(report_path), "The file /home/user/test_report.json is missing. Did you run pytest with the correct flags?"

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("test_report.json is not a valid JSON file.")

    assert "summary" in report, "The JSON report does not contain a 'summary' section."
    summary = report["summary"]

    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)

    assert passed == 3, f"Expected exactly 3 tests to pass, but found {passed} passed tests."
    assert failed == 0, f"Expected 0 failed tests, but found {failed} failed tests."