# test_final_state.py
import os
import json
import pytest

WORKSPACE = "/home/user/mobile_pipeline"
LIB_PATH = os.path.join(WORKSPACE, "libfastsemver.so")
RESOLVED_MANIFEST_PATH = os.path.join(WORKSPACE, "resolved_manifest.json")

def test_libfastsemver_exists():
    assert os.path.isfile(LIB_PATH), "The native extension libfastsemver.so was not built."

def test_resolved_manifest_exists():
    assert os.path.isfile(RESOLVED_MANIFEST_PATH), "The resolved_manifest.json file was not generated."

def test_resolved_manifest_content():
    expected_content = {
        "libAnalytics": "3.0.0",
        "libAuth": "1.2.9",
        "libDatabase": "4.2.0",
        "libNetwork": "2.1.10",
        "libUI": "1.15.2"
    }

    with open(RESOLVED_MANIFEST_PATH, 'r') as f:
        try:
            actual_content = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("resolved_manifest.json is not a valid JSON file.")

    assert actual_content == expected_content, (
        f"The resolved manifest content is incorrect.\n"
        f"Expected: {expected_content}\n"
        f"Actual: {actual_content}\n"
        f"Check your semantic version comparison logic."
    )

def test_resolved_manifest_formatting():
    with open(RESOLVED_MANIFEST_PATH, 'r') as f:
        raw_content = f.read()

    # Load and dump with sorted_keys=True and indent=4 to check exact formatting
    content_dict = json.loads(raw_content)
    expected_raw = json.dumps(content_dict, indent=4, sort_keys=True)

    assert raw_content.strip() == expected_raw.strip(), (
        "The resolved_manifest.json is not formatted correctly. "
        "Ensure it uses indent=4 and keys are sorted alphabetically."
    )