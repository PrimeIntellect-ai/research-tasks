# test_final_state.py

import os
import json
import urllib.request
import pytest

def test_files_moved_to_clean_project():
    """Check that the files were correctly moved based on the decoded JSON mapping."""
    auth_path = "/home/user/clean_project/backends/auth_service.py"
    user_path = "/home/user/clean_project/backends/user_service.py"

    assert os.path.isfile(auth_path), f"Expected file not found: {auth_path}"
    assert os.path.isfile(user_path), f"Expected file not found: {user_path}"

    # Ensure they were moved, not copied
    assert not os.path.exists("/home/user/messy_files/auth_service.py"), "auth_service.py should be moved, not copied."
    assert not os.path.exists("/home/user/messy_files/user_service.py"), "user_service.py should be moved, not copied."

def test_reverse_proxy_accuracy():
    """
    Test the reverse proxy routing accuracy.
    The proxy should be running on port 8000 and route /auth and /users correctly.
    """
    correct = 0
    total = 2

    # Test /auth route
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8000/auth", timeout=2)
        data = json.loads(req.read().decode())
        if data.get("service") == "auth":
            correct += 1
    except Exception as e:
        pass

    # Test /users route
    try:
        req = urllib.request.urlopen("http://127.0.0.1:8000/users", timeout=2)
        data = json.loads(req.read().decode())
        if data.get("service") == "user":
            correct += 1
    except Exception as e:
        pass

    accuracy = correct / total

    assert accuracy >= 1.0, f"Reverse proxy routing accuracy is {accuracy}, expected >= 1.0. Correctly routed {correct} out of {total} endpoints."