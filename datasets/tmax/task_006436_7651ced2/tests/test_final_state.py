# test_final_state.py

import os
import json
import pytest
import re

def test_artifacts_v2_schema_and_content():
    v1_path = "/home/user/artifacts_v1.json"
    v2_path = "/home/user/artifacts_v2.json"

    assert os.path.isfile(v1_path), f"Original file {v1_path} is missing."
    assert os.path.isfile(v2_path), f"Migrated file {v2_path} is missing."

    with open(v1_path, 'r') as f:
        v1_data = json.load(f)

    with open(v2_path, 'r') as f:
        try:
            v2_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{v2_path} is not valid JSON.")

    assert v2_data.get("schema_version") == "2.0", "schema_version is not '2.0'."
    assert "version" not in v2_data, "Old 'version' key should be removed."

    assert "artifacts" in v2_data, "'artifacts' key is missing."
    assert "items" not in v2_data, "Old 'items' key should be removed."

    v1_items = v1_data.get("items", [])
    v2_artifacts = v2_data.get("artifacts", [])

    assert len(v1_items) == len(v2_artifacts), "Number of artifacts does not match original items."

    for v1_item, v2_item in zip(v1_items, v2_artifacts):
        assert v2_item.get("identifier") == v1_item.get("id"), "identifier does not match original id."
        assert "id" not in v2_item, "Old 'id' key should be removed."

        assert v2_item.get("hash_value") == v1_item.get("checksum"), "hash_value does not match original checksum."
        assert "checksum" not in v2_item, "Old 'checksum' key should be removed."

        assert v2_item.get("hash_type") == v1_item.get("type"), "hash_type does not match original type."
        assert "type" not in v2_item, "Old 'type' key should be removed."

def test_verification_log_content():
    log_path = "/home/user/verification.log"
    assert os.path.isfile(log_path), f"Verification log {log_path} is missing."

    with open(log_path, 'r') as f:
        log_content = f.read()

    # Recompute expected output based on v1 data logic
    v1_path = "/home/user/artifacts_v1.json"
    with open(v1_path, 'r') as f:
        v1_data = json.load(f)

    for item in v1_data.get("items", []):
        checksum = item.get("checksum", "")
        # The C-extension logic: valid if length >= 8
        is_valid = len(checksum) >= 8
        status = "VALID" if is_valid else "INVALID"

        expected_line = f"Artifact {item['id']} ({item['type']}): {status}"
        assert expected_line in log_content, f"Expected line '{expected_line}' not found in verification.log."

def test_setup_py_fixed():
    setup_path = "/home/user/sec_artifact/setup.py"
    assert os.path.isfile(setup_path), f"setup.py is missing at {setup_path}."

    with open(setup_path, 'r') as f:
        content = f.read()

    # Check for packaging.version usage
    assert "packaging" in content and "version" in content, "setup.py does not appear to use packaging.version."
    assert "sys.version.split()[0] <" not in content, "setup.py still contains the naive version comparison bug."

    # Check for Extension usage
    assert "Extension" in content, "setup.py does not import or use setuptools.Extension."
    assert "verifier.c" in content or "sec_artifact/verifier.c" in content, "setup.py does not reference the verifier.c source file."