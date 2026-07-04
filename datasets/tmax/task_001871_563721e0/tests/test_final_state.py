# test_final_state.py

import os
import json
import pytest

PROJECT_DIR = "/home/user/project"

def test_directory_structure_and_files():
    """Verify that directories were created and files moved properly."""
    expected_structure = {
        "src": ["validator.c"],
        "include": ["validator.h"],
        "app": ["processor.py"],
        "data": ["limits.json", "requests.json", "results.json"],
        "lib": ["libvalidator.so"]
    }

    for dir_name, files in expected_structure.items():
        dir_path = os.path.join(PROJECT_DIR, dir_name)
        assert os.path.isdir(dir_path), f"Directory missing: {dir_path}"
        for filename in files:
            file_path = os.path.join(dir_path, filename)
            assert os.path.isfile(file_path), f"File missing: {file_path}"

def test_results_json_content():
    """Verify the output of the processor script."""
    results_path = os.path.join(PROJECT_DIR, "data", "results.json")
    assert os.path.isfile(results_path), f"Results file missing: {results_path}"

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not valid JSON")

    expected_results = [
        {"endpoint": "/api/login", "allowed": True},
        {"endpoint": "/api/login", "allowed": False},
        {"endpoint": "/api/data", "allowed": True},
        {"endpoint": "/api/admin", "allowed": False}
    ]

    assert results == expected_results, f"results.json content does not match expected output. Got: {results}"