# test_final_state.py
import os
import json
import pytest

def test_top_articles_json_exists_and_correct():
    output_path = "/home/user/top_articles.json"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {output_path} is not valid JSON.")

    assert isinstance(data, list), f"The JSON data should be a list, but got {type(data).__name__}."

    expected_data = [
        {
            "title": "Advances in Graph Databases",
            "year": 2019,
            "authors": "Dr. Alpha, Dr. Bravo",
            "citations": 4
        },
        {
            "title": "Machine Learning for RDF",
            "year": 2020,
            "authors": "Dr. Charlie",
            "citations": 3
        },
        {
            "title": "SPARQL Optimization Techniques",
            "year": 2019,
            "authors": "Dr. Alpha, Dr. Delta",
            "citations": 2
        }
    ]

    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert isinstance(actual, dict), f"Item at index {i} is not a JSON object."

        for key in ["title", "year", "authors", "citations"]:
            assert key in actual, f"Item at index {i} is missing the '{key}' key."
            assert actual[key] == expected[key], f"Item at index {i} has incorrect '{key}'. Expected {expected[key]}, got {actual[key]}."