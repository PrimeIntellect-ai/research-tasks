# test_final_state.py
import os
import json
import csv
from collections import defaultdict
import pytest

def compute_expected_results(csv_path):
    wrote = defaultdict(set)
    affiliated = defaultdict(set)

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 3:
                continue
            sub, rel, obj = row
            if rel == 'WROTE':
                wrote[obj].add(sub)
            elif rel == 'AFFILIATED_WITH':
                affiliated[obj].add(sub)

    author_inst = {}
    for inst, authors in affiliated.items():
        for a in authors:
            author_inst[a] = inst

    results = []
    for paper, authors in wrote.items():
        authors_list = sorted(list(authors))
        for i in range(len(authors_list)):
            for j in range(i+1, len(authors_list)):
                a1 = authors_list[i]
                a2 = authors_list[j]
                if a1 in author_inst and a2 in author_inst and author_inst[a1] == author_inst[a2]:
                    results.append({
                        "A1": a1,
                        "A2": a2,
                        "P": paper,
                        "I": author_inst[a1]
                    })

    results.sort(key=lambda x: (x["P"], x["I"], x["A1"], x["A2"]))
    return results[:3]

def test_output_json_exists_and_correct():
    csv_path = "/home/user/kg_edges.csv"
    json_path = "/home/user/output.json"

    assert os.path.isfile(csv_path), f"Input file {csv_path} is missing."
    assert os.path.isfile(json_path), f"Output file {json_path} is missing. Did the C program run and generate it?"

    expected_data = compute_expected_results(csv_path)

    with open(json_path, 'r') as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert isinstance(actual_data, list), "Output JSON must be an array of objects."
    assert len(actual_data) == len(expected_data), f"Expected {len(expected_data)} results, got {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."
        for key in ["A1", "A2", "P", "I"]:
            assert key in actual, f"Item at index {i} is missing key '{key}'."
            assert actual[key] == expected[key], f"Mismatch at index {i} for key '{key}': expected '{expected[key]}', got '{actual[key]}'."

def test_c_file_exists():
    c_path = "/home/user/find_pattern.c"
    assert os.path.isfile(c_path), f"Source file {c_path} is missing."