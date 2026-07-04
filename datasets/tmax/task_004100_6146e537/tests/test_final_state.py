# test_final_state.py
import os
import pytest
import requests

BASE_URL = "http://127.0.0.1:8080/evaluate"
AUTH_HEADER = {"Authorization": "Bearer 32"}

def test_makefile_exists():
    makefile_path = "/home/user/evaluator/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}."

def test_parser_patched():
    parser_path = "/home/user/evaluator/parser.cpp"
    assert os.path.isfile(parser_path), f"parser.cpp is missing at {parser_path}."
    with open(parser_path, "r") as f:
        content = f.read()
    assert "int result = left * right;" in content, "parser.cpp does not seem to be patched correctly with the multiplication fix."

def test_unauthorized_missing_header():
    try:
        response = requests.post(BASE_URL, data="7*6", timeout=5)
        assert response.status_code == 401, f"Expected 401 Unauthorized for missing auth header, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or request timed out: {e}")

def test_unauthorized_wrong_header():
    try:
        response = requests.post(BASE_URL, headers={"Authorization": "Bearer 999"}, data="7*6", timeout=5)
        assert response.status_code == 401, f"Expected 401 Unauthorized for incorrect auth header, got {response.status_code}. Response: {response.text}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or request timed out: {e}")

def test_authorized_evaluate_multiplication():
    try:
        response = requests.post(BASE_URL, headers=AUTH_HEADER, data="7*6", timeout=5)
        assert response.status_code == 200, f"Expected 200 OK for valid request, got {response.status_code}. Response: {response.text}"
        assert response.text.strip() == "42", f"Expected '42' as the evaluation result, got '{response.text}'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or request timed out: {e}")

def test_authorized_evaluate_addition():
    try:
        response = requests.post(BASE_URL, headers=AUTH_HEADER, data="10+15", timeout=5)
        assert response.status_code == 200, f"Expected 200 OK for valid request, got {response.status_code}. Response: {response.text}"
        assert response.text.strip() == "25", f"Expected '25' as the evaluation result, got '{response.text}'"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the server or request timed out: {e}")