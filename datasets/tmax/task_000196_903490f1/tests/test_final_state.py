# test_final_state.py

import os
import json
import pytest

def calc_signature(data: bytes) -> int:
    """Calculates the custom artifact signature as defined in the task."""
    sig = sum(b * (i + 1) for i, b in enumerate(data))
    return sig % 1000003

def test_build_script_effects():
    """Verify that build.sh correctly initialized the module and built the executable."""
    go_mod_path = "/home/user/manager/go.mod"
    assert os.path.exists(go_mod_path), f"Go module file {go_mod_path} does not exist. build.sh may not have run correctly."

    with open(go_mod_path, 'r') as f:
        go_mod_content = f.read()
    assert "module manager" in go_mod_content, "go.mod does not contain 'module manager'."

    executable_path = "/home/user/manager/artifact-server"
    assert os.path.exists(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_final_manifest_content():
    """Verify that the final manifest JSON exists and contains the correct signatures."""
    manifest_path = "/home/user/final_manifest.json"
    assert os.path.exists(manifest_path), f"Final manifest file {manifest_path} does not exist."

    with open(manifest_path, 'r') as f:
        try:
            manifest_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {manifest_path} does not contain valid JSON.")

    artifacts_dir = "/home/user/manager/artifacts"
    assert os.path.exists(artifacts_dir), f"Artifacts directory {artifacts_dir} does not exist."

    expected_manifest = {}
    for filename in os.listdir(artifacts_dir):
        if filename.endswith(".bin"):
            filepath = os.path.join(artifacts_dir, filename)
            with open(filepath, 'rb') as f:
                data = f.read()
            expected_manifest[filename] = calc_signature(data)

    assert isinstance(manifest_data, dict), "Manifest JSON should be an object (dictionary)."

    for filename, expected_sig in expected_manifest.items():
        assert filename in manifest_data, f"Artifact {filename} is missing from the final manifest."
        assert manifest_data[filename] == expected_sig, f"Incorrect signature for {filename}. Expected {expected_sig}, got {manifest_data[filename]}."

    # Verify no extra keys are present
    for key in manifest_data.keys():
        assert key in expected_manifest, f"Unexpected artifact {key} found in the final manifest."