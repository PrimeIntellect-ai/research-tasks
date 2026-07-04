# test_final_state.py

import os
import json
import urllib.request
import pytest

def test_ci_report():
    report_path = "/home/user/ci_report.json"
    assert os.path.isfile(report_path), f"CI report {report_path} does not exist."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("CI report is not valid JSON.")

    assert data.get("backend_ok") is True, "backend_ok is not true in CI report."
    assert data.get("static_ok") is True, "static_ok is not true in CI report."
    assert data.get("symlink_valid") is True, "symlink_valid is not true in CI report."

def test_symlink_fixed():
    symlink_path = "/home/user/web_root/public"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    assert target == "/home/user/app/static", f"Symlink points to {target}, expected /home/user/app/static."
    assert os.path.isdir(symlink_path), f"Symlink {symlink_path} does not resolve to a valid directory."

def test_live_endpoints():
    # Test backend proxy
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/", timeout=5)
        body = req.read().decode("utf-8")
        assert req.getcode() == 200, f"Expected status 200 for backend, got {req.getcode()}"
        assert "Backend is alive" in body, "Backend response does not contain 'Backend is alive'."
    except Exception as e:
        pytest.fail(f"Failed to connect to backend via Nginx: {e}")

    # Test static file serving
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8080/static/index.html", timeout=5)
        body = req.read().decode("utf-8")
        assert req.getcode() == 200, f"Expected status 200 for static file, got {req.getcode()}"
        assert "Hello from static" in body, "Static response does not contain 'Hello from static'."
    except Exception as e:
        pytest.fail(f"Failed to connect to static file via Nginx: {e}")