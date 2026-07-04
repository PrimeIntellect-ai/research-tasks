# test_final_state.py

import os
import json
import pytest

def test_cpp_source_and_executable_exist():
    source_path = "/home/user/graph_optimizer.cpp"
    executable_path = "/home/user/graph_optimizer"

    assert os.path.exists(source_path), f"Source file {source_path} is missing."
    assert os.path.isfile(source_path), f"Path {source_path} is not a file."

    assert os.path.exists(executable_path), f"Executable file {executable_path} is missing. Did you compile the code?"
    assert os.path.isfile(executable_path), f"Path {executable_path} is not a file."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_optimization_report_json():
    report_path = "/home/user/optimization_report.json"

    assert os.path.exists(report_path), f"The output JSON file {report_path} is missing."
    assert os.path.isfile(report_path), f"Path {report_path} is not a file."

    with open(report_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"File {report_path} does not contain valid JSON. Error: {e}")

    assert "top_dependencies" in data, "Key 'top_dependencies' is missing in the JSON output."
    assert "shortest_path" in data, "Key 'shortest_path' is missing in the JSON output."

    expected_top_dependencies = [
        "raw_transactions",
        "clean_transactions",
        "regional_sales_view"
    ]

    expected_shortest_path = [
        "monthly_sales_report",
        "regional_sales_view",
        "clean_transactions",
        "raw_transactions"
    ]

    assert data["top_dependencies"] == expected_top_dependencies, \
        f"Expected top_dependencies to be {expected_top_dependencies}, but got {data['top_dependencies']}"

    assert data["shortest_path"] == expected_shortest_path, \
        f"Expected shortest_path to be {expected_shortest_path}, but got {data['shortest_path']}"