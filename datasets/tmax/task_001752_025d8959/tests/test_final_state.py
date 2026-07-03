# test_final_state.py

import os
import json
import subprocess
import pytest

MIGRATOR_DIR = "/home/user/migrator"

def test_go_build_succeeds():
    """Test that the Go project compiles successfully."""
    result = subprocess.run(
        ["go", "build"],
        cwd=MIGRATOR_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"go build failed with error:\n{result.stderr}"

def test_go_test_succeeds():
    """Test that the property-based tests pass."""
    result = subprocess.run(
        ["go", "test"],
        cwd=MIGRATOR_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"go test failed with error:\n{result.stderr}\n{result.stdout}"

def test_modern_json_exists_and_correct():
    """Test that modern.json is correctly generated and sorted."""
    modern_json_path = os.path.join(MIGRATOR_DIR, "modern.json")
    assert os.path.isfile(modern_json_path), f"{modern_json_path} does not exist."

    with open(modern_json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("modern.json is not valid JSON.")

    assert isinstance(data, list), "modern.json should contain a JSON array."

    # Check ID 1
    id_1_records = [r for r in data if r.get("id") == 1]
    assert len(id_1_records) == 1, "There should be exactly one merged record for ID 1."

    record_1 = id_1_records[0]
    # MergedData order can depend on map iteration, but values must be sorted
    assert "merged_data" in record_1, "Missing merged_data in modern.json record."
    assert set(record_1["merged_data"]) == set("AC"), "merged_data for ID 1 should contain 'A' and 'C'."

    assert "sorted_values" in record_1, "Missing sorted_values in modern.json record."
    assert record_1["sorted_values"] == [1, 2, 5, 7, 9], "sorted_values for ID 1 is not correctly merged and sorted."

    # Check ID 2
    id_2_records = [r for r in data if r.get("id") == 2]
    assert len(id_2_records) == 1, "There should be exactly one merged record for ID 2."

    record_2 = id_2_records[0]
    assert record_2["merged_data"] == "B", "merged_data for ID 2 should be 'B'."
    assert record_2["sorted_values"] == [8], "sorted_values for ID 2 is incorrect."

def test_migration_diff_exists_and_valid():
    """Test that migration.diff exists and contains a unified diff."""
    diff_path = os.path.join(MIGRATOR_DIR, "migration.diff")
    assert os.path.isfile(diff_path), f"{diff_path} does not exist."

    with open(diff_path, 'r') as f:
        diff_content = f.read()

    assert len(diff_content.strip()) > 0, "migration.diff is empty."

    # A unified diff typically starts with --- and +++
    has_minus = any(line.startswith("--- ") for line in diff_content.splitlines())
    has_plus = any(line.startswith("+++ ") for line in diff_content.splitlines())

    assert has_minus and has_plus, "migration.diff does not appear to be a valid unified diff format."