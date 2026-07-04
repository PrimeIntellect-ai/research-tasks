# test_final_state.py

import os
import json
import pytest

ARTIFACTS_DIR = "/home/user/artifacts"
BUILD_ORDER_FILE = "/home/user/build_order.txt"

def test_libB_schema_migration():
    filepath = os.path.join(ARTIFACTS_DIR, "libB.json")
    assert os.path.isfile(filepath), f"File {filepath} is missing."
    with open(filepath, "r") as f:
        data = json.load(f)

    assert data.get("schema_version") == 2, f"libB.json schema_version should be 2, got {data.get('schema_version')}"
    assert "needs" not in data, "libB.json should not contain 'needs' key."
    assert "requires" in data, "libB.json should contain 'requires' key."
    assert data.get("requires") == ["A"], f"libB.json requires should be ['A'], got {data.get('requires')}"
    assert data.get("name") == "libB", "libB.json name should remain 'libB'"
    assert data.get("provides") == ["B"], "libB.json provides should remain ['B']"

def test_libD_dependency_fix():
    filepath = os.path.join(ARTIFACTS_DIR, "libD.json")
    assert os.path.isfile(filepath), f"File {filepath} is missing."
    with open(filepath, "r") as f:
        data = json.load(f)

    assert data.get("schema_version") == 2, "libD.json schema_version should be 2"
    assert "requires" in data, "libD.json should contain 'requires' key."
    assert data.get("requires") == ["A"], f"libD.json requires should be ['A'] instead of ['C'], got {data.get('requires')}"

def test_build_order_output():
    assert os.path.isfile(BUILD_ORDER_FILE), f"File {BUILD_ORDER_FILE} is missing."
    with open(BUILD_ORDER_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_order = ["libA", "libB", "libD", "libC"]
    assert lines == expected_order, f"Build order is incorrect. Expected {expected_order}, got {lines}"