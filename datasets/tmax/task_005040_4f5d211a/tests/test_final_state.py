# test_final_state.py

import os
import json
import sqlite3
import pytest

def sort_deps(d):
    """Recursively sort the dependencies list to ensure order-independent comparison."""
    if "dependencies" in d:
        d["dependencies"].sort(key=lambda x: x.get("job", ""))
        for child in d["dependencies"]:
            sort_deps(child)
    return d

def test_c_source_exists_and_uses_prepared_statements():
    source_path = "/home/user/export_graph.c"
    assert os.path.exists(source_path), f"C source file missing at {source_path}"

    with open(source_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for usage of prepared statements
    assert "sqlite3_prepare" in content, "C program must use sqlite3_prepare_v2 or similar to prepare statements."
    assert "sqlite3_bind_" in content, "C program must use parameterized queries (e.g., sqlite3_bind_int, sqlite3_bind_text)."

def test_executable_exists():
    exec_path = "/home/user/export_graph"
    assert os.path.exists(exec_path), f"Compiled executable missing at {exec_path}"
    assert os.access(exec_path, os.X_OK), f"File at {exec_path} is not executable"

def test_json_output_correctness():
    json_path = "/home/user/dependency_doc.json"
    assert os.path.exists(json_path), f"JSON output file missing at {json_path}"

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    sorted_data = sort_deps(data)

    expected = {
        "job": "app_server_backup",
        "dependencies": [
            {
                "job": "auth_service",
                "dependencies": [
                    {
                        "job": "network_storage_A",
                        "dependencies": []
                    }
                ]
            },
            {
                "job": "db_cluster_1",
                "dependencies": [
                    {
                        "job": "network_storage_A",
                        "dependencies": []
                    }
                ]
            }
        ]
    }

    assert sorted_data == expected, "JSON output does not match the expected dependency graph structure."