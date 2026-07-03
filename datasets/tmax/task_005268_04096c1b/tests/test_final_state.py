# test_final_state.py

import os
import json
import pytest

def test_recover_cpp_exists():
    """Verify that the C++ program recover.cpp was created."""
    file_path = "/home/user/recover.cpp"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

def test_restored_json_valid():
    """Verify that restored.json exists and contains the correct JSON data."""
    file_path = "/home/user/artifacts/restored.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} does not contain valid JSON.")

    assert "repository" in data, "JSON missing 'repository' key."
    assert data["repository"] == "core-binaries", "Incorrect 'repository' value."
    assert "artifacts" in data, "JSON missing 'artifacts' key."

    # Check if the specific artifact is present
    found = False
    for artifact in data["artifacts"]:
        if artifact.get("id") == "linux-kernel-6.5-rc1":
            found = True
            assert artifact.get("sha256_checksum") == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855", "Incorrect checksum in JSON."
            break

    assert found, "Artifact 'linux-kernel-6.5-rc1' not found in restored JSON."

def test_flag_txt_correct():
    """Verify that flag.txt exists and contains the correct checksum."""
    file_path = "/home/user/artifacts/flag.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_checksum = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert content == expected_checksum, f"Expected {expected_checksum} in flag.txt, but got {content}."