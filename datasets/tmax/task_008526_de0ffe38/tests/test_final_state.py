# test_final_state.py

import os
import json
import subprocess
import pytest

AUTH_SERVICE_DIR = "/home/user/auth-service"
RESOLUTION_FILE = "/home/user/resolution.json"

def test_go_build_success():
    """Test that go build runs successfully without linker errors."""
    assert os.path.isdir(AUTH_SERVICE_DIR), f"Directory {AUTH_SERVICE_DIR} does not exist."

    try:
        result = subprocess.run(
            ["go", "build"],
            cwd=AUTH_SERVICE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'go build' failed with exit code {e.returncode}. Stderr: {e.stderr}")

def test_go_test_race_success():
    """Test that go test -race passes reliably."""
    try:
        result = subprocess.run(
            ["go", "test", "-race", "./..."],
            cwd=AUTH_SERVICE_DIR,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'go test -race ./...' failed with exit code {e.returncode}. Stderr: {e.stderr}\nStdout: {e.stdout}")

def test_main_go_cgo_removed():
    """Test that CGO directives are removed from main.go."""
    main_go_path = os.path.join(AUTH_SERVICE_DIR, "main.go")
    assert os.path.isfile(main_go_path), f"File {main_go_path} does not exist."

    with open(main_go_path, "r") as f:
        content = f.read()

    assert "#cgo" not in content, "CGO directives (#cgo) are still present in main.go."
    assert "import \"C\"" not in content, "import \"C\" is still present in main.go."

def test_auth_go_mutex_added():
    """Test that a mutex is used in auth.go to protect tokenCache."""
    auth_go_path = os.path.join(AUTH_SERVICE_DIR, "auth.go")
    assert os.path.isfile(auth_go_path), f"File {auth_go_path} does not exist."

    with open(auth_go_path, "r") as f:
        content = f.read()

    has_mutex = "sync.Mutex" in content or "sync.RWMutex" in content or "sync.Map" in content
    assert has_mutex, "auth.go does not seem to use sync.Mutex, sync.RWMutex, or sync.Map to fix the race condition."

def test_resolution_json_contents():
    """Test that resolution.json exists and contains the correct answers."""
    assert os.path.isfile(RESOLUTION_FILE), f"File {RESOLUTION_FILE} does not exist."

    with open(RESOLUTION_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{RESOLUTION_FILE} is not a valid JSON file.")

    assert "build_fix" in data, "Key 'build_fix' missing in resolution.json"
    assert "bug_type" in data, "Key 'bug_type' missing in resolution.json"
    assert "fixed_variable" in data, "Key 'fixed_variable' missing in resolution.json"

    build_fix = str(data["build_fix"]).lower()
    bug_type = str(data["bug_type"]).lower()
    fixed_var = str(data["fixed_variable"])

    assert "main.go" in build_fix or "cgo" in build_fix, f"Expected 'build_fix' to mention main.go or cgo, got: {data['build_fix']}"
    assert "race" in bug_type, f"Expected 'bug_type' to mention race condition, got: {data['bug_type']}"
    assert fixed_var == "tokenCache", f"Expected 'fixed_variable' to be 'tokenCache', got: {data['fixed_variable']}"