# test_final_state.py

import os
import stat
import subprocess
import json
import pytest

SCRIPT_PATH = "/home/user/solver.sh"

def run_solver(http_request: str) -> str:
    result = subprocess.run(
        [SCRIPT_PATH],
        input=http_request,
        text=True,
        capture_output=True,
        check=False
    )
    return result.stdout

def parse_http_response(stdout: str):
    # Normalize line endings
    stdout = stdout.replace("\r\n", "\n")
    parts = stdout.split("\n\n", 1)

    headers_part = parts[0]
    body = parts[1] if len(parts) > 1 else ""

    header_lines = headers_part.split("\n")
    status_line = header_lines[0] if header_lines else ""
    headers = [line.lower() for line in header_lines[1:]]

    return status_line, headers, body.strip()

def test_script_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."
    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {SCRIPT_PATH} is not executable."

def test_valid_200_ok():
    req = "GET /api/v1/fit?libs=math,crypto,net&max=200 HTTP/1.1\r\nHost: localhost\r\n\r\n"
    stdout = run_solver(req)
    status_line, headers, body = parse_http_response(stdout)

    assert "200 OK" in status_line, f"Expected 200 OK, got: {status_line}"
    assert any("content-type: application/json" in h for h in headers), "Missing or incorrect Content-Type header."

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Could not parse JSON body: {body}")

    assert data.get("status") == "ok", "Expected status 'ok'"
    assert data.get("total") == 100, f"Expected total 100, got {data.get('total')}"

def test_valid_400_bad_request():
    req = "GET /api/v1/fit?libs=db,ui,core&max=150 HTTP/1.1\r\nHost: localhost\r\n\r\n"
    stdout = run_solver(req)
    status_line, headers, body = parse_http_response(stdout)

    assert "400 Bad Request" in status_line, f"Expected 400 Bad Request, got: {status_line}"
    assert any("content-type: application/json" in h for h in headers), "Missing or incorrect Content-Type header."

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Could not parse JSON body: {body}")

    assert data.get("error") == "exceeds capacity", "Expected error 'exceeds capacity'"
    assert data.get("total") == 250, f"Expected total 250, got {data.get('total')}"
    assert data.get("max") == 150, f"Expected max 150, got {data.get('max')}"

def test_404_not_found():
    req = "GET /api/v1/other?libs=math&max=200 HTTP/1.1\r\nHost: localhost\r\n\r\n"
    stdout = run_solver(req)
    status_line, headers, body = parse_http_response(stdout)

    assert "404 Not Found" in status_line, f"Expected 404 Not Found, got: {status_line}"
    assert body == "", "Expected empty body for 404 Not Found"

def test_missing_libraries_ignored():
    req = "GET /api/v1/fit?libs=core,nonexistent,net&max=100 HTTP/1.1\r\nHost: localhost\r\n\r\n"
    stdout = run_solver(req)
    status_line, headers, body = parse_http_response(stdout)

    assert "200 OK" in status_line, f"Expected 200 OK, got: {status_line}"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail(f"Could not parse JSON body: {body}")

    assert data.get("status") == "ok", "Expected status 'ok'"
    assert data.get("total") == 75, f"Expected total 75, got {data.get('total')}"