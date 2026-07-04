# test_final_state.py

import os
import json
import pytest

V2_INDEX_PATH = "/home/user/v2_index.json"
TRANSITIVE_DEPS_PATH = "/home/user/transitive_deps.log"
LEGACY_INDEX_PATH = "/home/user/legacy_index.json"

def test_legacy_index_unmodified():
    assert os.path.isfile(LEGACY_INDEX_PATH), f"Legacy index file missing at {LEGACY_INDEX_PATH}"
    with open(LEGACY_INDEX_PATH, 'r') as f:
        data = json.load(f)
    assert "packages" in data, "Legacy index format has been altered."

def test_v2_index_schema_and_data():
    assert os.path.isfile(V2_INDEX_PATH), f"New index file missing at {V2_INDEX_PATH}"

    with open(V2_INDEX_PATH, 'r') as f:
        try:
            v2_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{V2_INDEX_PATH} is not valid JSON.")

    assert "artifacts" in v2_data, f"Key 'artifacts' not found in {V2_INDEX_PATH}"
    artifacts = v2_data["artifacts"]
    assert isinstance(artifacts, list), "'artifacts' should be a list."

    # Check that all expected packages are present and properly formatted
    expected_data = {
        "lib-alpha": {"version": "1.0", "dependencies": ["lib-beta", "lib-gamma"]},
        "lib-beta": {"version": "2.2", "dependencies": ["lib-delta"]},
        "lib-gamma": {"version": "1.1", "dependencies": []},
        "lib-delta": {"version": "3.0", "dependencies": ["lib-gamma"]},
        "lib-core": {"version": "0.9", "dependencies": ["lib-alpha", "lib-epsilon"]},
        "lib-epsilon": {"version": "4.1", "dependencies": []}
    }

    assert len(artifacts) == len(expected_data), f"Expected {len(expected_data)} artifacts, found {len(artifacts)}"

    actual_data = {}
    for item in artifacts:
        assert "name" in item, "Artifact missing 'name' key"
        assert "version" in item, f"Artifact {item.get('name')} missing 'version' key"
        assert "dependencies" in item, f"Artifact {item.get('name')} missing 'dependencies' key"
        actual_data[item["name"]] = {
            "version": item["version"],
            "dependencies": item["dependencies"]
        }

    for pkg, details in expected_data.items():
        assert pkg in actual_data, f"Package {pkg} missing from v2_index.json"
        assert actual_data[pkg]["version"] == details["version"], f"Incorrect version for {pkg}"
        assert sorted(actual_data[pkg]["dependencies"]) == sorted(details["dependencies"]), f"Incorrect dependencies for {pkg}"

def test_transitive_deps_log():
    assert os.path.isfile(TRANSITIVE_DEPS_PATH), f"Log file missing at {TRANSITIVE_DEPS_PATH}"

    with open(TRANSITIVE_DEPS_PATH, 'r') as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected_deps = [
        "lib-alpha",
        "lib-beta",
        "lib-delta",
        "lib-epsilon",
        "lib-gamma"
    ]

    assert lines == expected_deps, f"Expected dependencies {expected_deps}, but got {lines}"