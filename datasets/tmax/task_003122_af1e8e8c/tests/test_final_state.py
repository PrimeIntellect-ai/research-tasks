# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_ci_success_log_exists():
    log_path = os.path.join(PROJECT_DIR, "ci_success.log")
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did you run ci_run.sh?"

    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "CI SUCCESS", f"Expected 'CI SUCCESS' in {log_path}, got '{content}'"

def test_build_artifacts_exist():
    url_tool = os.path.join(PROJECT_DIR, "url_tool")
    lib_so = os.path.join(PROJECT_DIR, "liburlsanitizer.so")

    assert os.path.isfile(url_tool), "url_tool binary is missing. Did build.sh succeed?"
    assert os.access(url_tool, os.X_OK), "url_tool is not executable."
    assert os.path.isfile(lib_so), "liburlsanitizer.so is missing."

def test_url_tool_runs_correctly():
    # Verify that url_tool can run without LD_LIBRARY_PATH (rpath or similar is set)
    url_tool = os.path.join(PROJECT_DIR, "url_tool")

    # Run from a different directory to ensure rpath or absolute paths work if needed, 
    # but the prompt implies we run it from the project dir. Let's run it from PROJECT_DIR.
    try:
        result = subprocess.run(
            ["./url_tool", "/test/path"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        assert result.stdout.strip() == "/test/path", "url_tool did not output the expected path."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"url_tool execution failed: {e.stderr}. Is the shared library linked correctly?")

def test_test_routing_strips_query_params():
    test_script = os.path.join(PROJECT_DIR, "test_routing.sh")

    try:
        result = subprocess.run(
            ["./test_routing.sh", "http://example.com/some/path?param=value"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=True
        )
        assert result.stdout.strip() == "/some/path", f"test_routing.sh failed to strip query params. Output: {result.stdout.strip()}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"test_routing.sh execution failed: {e.stderr}")

def test_ci_run_script_succeeds():
    ci_script = os.path.join(PROJECT_DIR, "ci_run.sh")
    try:
        subprocess.run(
            ["./ci_run.sh"],
            cwd=PROJECT_DIR,
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"ci_run.sh failed when executed: {e.stdout}\n{e.stderr}")