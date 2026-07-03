# test_final_state.py

import os
import subprocess
import json
import pytest

APP_DIR = "/home/user/app"
FIXTURE_DIR = os.path.join(APP_DIR, "fixtures")
FIXTURE_FILE = os.path.join(FIXTURE_DIR, "schema_v1.json")
PATCH_FILE = "/home/user/router.patch"
TEST_SCRIPT = os.path.join(APP_DIR, "test.sh")

def test_fixture_exists_and_correct():
    assert os.path.isdir(FIXTURE_DIR), f"Directory {FIXTURE_DIR} was not created."
    assert os.path.isfile(FIXTURE_FILE), f"File {FIXTURE_FILE} was not created."

    with open(FIXTURE_FILE, "r") as f:
        content = f.read().strip()

    try:
        data = json.loads(content)
        assert data == {"version": 1}, f"Fixture content is incorrect. Expected {{'version': 1}}, got {data}"
    except json.JSONDecodeError:
        # If it's not valid JSON but exactly matches the string
        assert content == '{"version": 1}', f"Fixture content is incorrect. Expected '{{\"version\": 1}}', got '{content}'"

def test_patch_file_exists_and_valid():
    assert os.path.isfile(PATCH_FILE), f"Patch file {PATCH_FILE} was not created."

    with open(PATCH_FILE, "r") as f:
        content = f.read()

    assert "---" in content and "+++" in content, f"Patch file {PATCH_FILE} does not look like a valid unified diff."
    assert "router.sh" in content, f"Patch file {PATCH_FILE} does not seem to contain changes for router.sh."

def test_test_script_passes():
    assert os.path.isfile(TEST_SCRIPT), f"Test script {TEST_SCRIPT} is missing."

    result = subprocess.run(
        [TEST_SCRIPT],
        cwd=APP_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"test.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"
    assert "All tests passed." in result.stdout, f"test.sh did not print 'All tests passed.'.\nOutput: {result.stdout}"