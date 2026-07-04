# test_final_state.py
import os
import json

def test_schema_output_exists():
    output_path = "/home/user/schema_output.json"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist."
    assert os.path.isfile(output_path), f"The path {output_path} is not a file."

def test_schema_output_content():
    output_path = "/home/user/schema_output.json"

    with open(output_path, 'r') as f:
        try:
            actual = json.load(f)
        except json.JSONDecodeError as e:
            assert False, f"Failed to parse {output_path} as JSON: {e}"

    expected = {
        "http://example.org/Institution": [
            "http://example.org/orgName",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        ],
        "http://example.org/Paper": [
            "http://example.org/author",
            "http://example.org/title",
            "http://example.org/year",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        ],
        "http://example.org/Researcher": [
            "http://example.org/name",
            "http://example.org/worksAt",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        ]
    }

    # Sort the lists in the expected and actual to ensure order doesn't fail the test if they are out of order,
    # although the requirements say they should be sorted.
    for key in expected:
        expected[key] = sorted(expected[key])

    for key in actual:
        if isinstance(actual[key], list):
            # Check if the list is actually sorted as per requirements
            assert actual[key] == sorted(actual[key]), f"The list of predicates for {key} is not alphabetically sorted."

    assert actual == expected, f"The content of {output_path} does not match the expected schema. Expected: {expected}, Actual: {actual}"