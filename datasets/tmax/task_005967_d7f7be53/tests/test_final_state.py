# test_final_state.py
import os
import json
import csv
import pytest

def test_active_edges_csv():
    csv_path = "/home/user/active_edges.csv"
    assert os.path.isfile(csv_path), f"CSV file {csv_path} is missing."

    expected_edges = {
        ("1", "2"), ("2", "3"), ("3", "1"),
        ("2", "4"), ("4", "6"), ("6", "2"),
        ("4", "7"), ("7", "1"), ("1", "6"),
        ("7", "2")
    }

    actual_edges = set()
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                assert len(row) == 2, f"Invalid row format in CSV: {row}"
                actual_edges.add((row[0].strip(), row[1].strip()))

    assert actual_edges == expected_edges, f"CSV edges do not match expected. Missing: {expected_edges - actual_edges}, Unexpected: {actual_edges - expected_edges}"

def test_c_program_exists():
    c_path = "/home/user/find_triangles.c"
    exe_path = "/home/user/find_triangles"

    assert os.path.isfile(c_path), f"C source file {c_path} is missing."
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_triangles_jsonl():
    jsonl_path = "/home/user/triangles.jsonl"
    assert os.path.isfile(jsonl_path), f"JSONL file {jsonl_path} is missing."

    expected_triangles = {
        tuple([1, 2, 3]),
        tuple([2, 4, 6])
    }

    actual_triangles = set()
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Invalid JSON line in {jsonl_path}: {line}")

            assert "triangle" in data, f"Missing 'triangle' key in JSON line: {line}"
            actual_triangles.add(tuple(data["triangle"]))

    assert actual_triangles == expected_triangles, f"Triangles in JSONL do not match expected. Found: {actual_triangles}"

def test_final_report_json():
    report_path = "/home/user/final_report.json"
    assert os.path.isfile(report_path), f"Final report JSON {report_path} is missing."

    with open(report_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON in {report_path}")

    assert "metadata" in data, "Missing 'metadata' key in final report."
    assert "total_triangles" in data["metadata"], "Missing 'total_triangles' in metadata."
    assert data["metadata"]["total_triangles"] == 2, f"Expected 2 total triangles, got {data['metadata']['total_triangles']}"

    assert "data" in data, "Missing 'data' key in final report."

    expected_data = [
        [1, 2, 3],
        [2, 4, 6]
    ]

    assert data["data"] == expected_data, f"Data array does not match expected. Got: {data['data']}"