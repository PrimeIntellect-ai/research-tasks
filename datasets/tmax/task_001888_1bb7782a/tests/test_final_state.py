# test_final_state.py

import os
import json
import subprocess
import pytest

def test_build_manifest_exists_and_correct():
    """Check that build_manifest.json exists and contains the expected output."""
    manifest_path = "/home/user/build_manifest.json"
    assert os.path.isfile(manifest_path), f"File {manifest_path} does not exist. Did you run your script?"

    with open(manifest_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{manifest_path} does not contain valid JSON.")

    expected_data = {
        "app.bld": {
            "target": "arm64",
            "emitted_files": ["base_binary", "linux_bindings.so"]
        },
        "tools.bld": {
            "target": "x86_64",
            "emitted_files": ["tool_main", "debug_symbols.pdb"]
        },
        "utils.bld": {
            "target": None,
            "emitted_files": ["wrapper.py"]
        }
    }

    # Validate structure and content
    for key, expected_val in expected_data.items():
        assert key in data, f"Manifest is missing key: '{key}'"
        actual_val = data[key]

        assert "target" in actual_val, f"Key '{key}' missing 'target' field."
        assert actual_val["target"] == expected_val["target"], \
            f"Expected target {expected_val['target']} for {key}, got {actual_val['target']}."

        assert "emitted_files" in actual_val, f"Key '{key}' missing 'emitted_files' field."
        assert isinstance(actual_val["emitted_files"], list), \
            f"'emitted_files' for {key} should be a list."

        assert sorted(actual_val["emitted_files"]) == sorted(expected_val["emitted_files"]), \
            f"Expected emitted_files {expected_val['emitted_files']} for {key}, got {actual_val['emitted_files']}."

def test_organizer_script_exists():
    """Check that organizer.py exists."""
    script_path = "/home/user/organizer.py"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."

def test_unittest_script_exists_and_passes():
    """Check that test_organizer.py exists and runs successfully with unittest."""
    test_script_path = "/home/user/test_organizer.py"
    assert os.path.isfile(test_script_path), f"File {test_script_path} does not exist."

    # Run the unittest
    result = subprocess.run(
        ["python3", "-m", "unittest", test_script_path],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, \
        f"Unittests failed. Return code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"

    assert "OK" in result.stderr or "OK" in result.stdout, \
        "Unittest output did not indicate success ('OK')."