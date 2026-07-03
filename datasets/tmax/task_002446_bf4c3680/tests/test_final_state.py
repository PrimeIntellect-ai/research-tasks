# test_final_state.py

import os
import json

def test_ai_authors_json_exists_and_correct():
    json_path = "/home/user/ai_authors.json"
    assert os.path.isfile(json_path), f"Expected output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} does not contain valid JSON."

    expected_data = {
        "Ada Lovelace": [
            "Advanced LLMs",
            "Notes on the Analytical Engine"
        ],
        "Alan Turing": [
            "Computing Machinery and Intelligence",
            "Deep Neural Nets",
            "The Imitation Game"
        ]
    }

    assert isinstance(data, dict), "The top-level JSON structure should be a dictionary/object."

    # Check that only the expected authors are present
    assert set(data.keys()) == set(expected_data.keys()), f"Expected authors {list(expected_data.keys())}, but got {list(data.keys())}."

    for author, expected_papers in expected_data.items():
        actual_papers = data.get(author)
        assert isinstance(actual_papers, list), f"The value for '{author}' must be a list of strings."

        # The prompt requires the array of paper titles to be sorted alphabetically.
        assert actual_papers == sorted(actual_papers), f"The paper titles for '{author}' are not sorted alphabetically."

        # Check exact match of papers
        assert actual_papers == expected_papers, f"Expected papers {expected_papers} for '{author}', but got {actual_papers}."

def test_json_formatting():
    json_path = "/home/user/ai_authors.json"
    assert os.path.isfile(json_path), f"Expected output file {json_path} does not exist."

    with open(json_path, 'r') as f:
        content = f.read()

    # A basic check to ensure the file is nicely formatted (contains newlines)
    assert "\n" in content, "The JSON file should be nicely formatted (e.g., indent=2), but no newlines were found."