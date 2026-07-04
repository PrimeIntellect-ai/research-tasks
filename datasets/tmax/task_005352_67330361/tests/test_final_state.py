# test_final_state.py

import os
import json

def test_graph_etl_cpp_exists():
    assert os.path.isfile("/home/user/graph_etl.cpp"), "/home/user/graph_etl.cpp does not exist."

def test_run_pipeline_sh_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_reports_json_content():
    json_path = "/home/user/reports.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    expected_data = [
        {"emp_id": 10, "name": "Judy", "salary": 115000},
        {"emp_id": 5, "name": "Eve", "salary": 110000},
        {"emp_id": 8, "name": "Heidi", "salary": 105000}
    ]

    assert data == expected_data, f"Content of {json_path} does not match expected output. Got: {data}"

def test_final_report_txt_content():
    txt_path = "/home/user/final_report.txt"
    assert os.path.isfile(txt_path), f"{txt_path} does not exist."

    with open(txt_path, "r") as f:
        lines = [line.strip().replace('"', '') for line in f if line.strip()]

    expected_lines = ["Judy", "Eve", "Heidi"]

    assert lines == expected_lines, f"Content of {txt_path} does not match expected output. Got: {lines}"