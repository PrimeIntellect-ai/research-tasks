# test_final_state.py

import os
import json

def test_top_authors_exists_and_valid():
    output_path = "/home/user/top_authors.json"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. The pipeline must generate this file."

    with open(output_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{output_path} is not a valid JSON file."

    assert isinstance(data, list), f"The output in {output_path} must be a JSON array."
    assert len(data) == 3, f"The output must contain exactly 3 items, but found {len(data)}."

    # Expected logic:
    # Alice_Smith: cited by p2, p3, p11 (all Science) -> 3
    # Eve_Davis: cited by p5, p7, p8 (all Science) -> 3
    # Ivan_Drago: cited by p11 (Science) -> 1
    # Tie breaking: Alice_Smith comes before Eve_Davis alphabetically.

    expected = [
        {"author": "Alice_Smith", "science_citations": 3},
        {"author": "Eve_Davis", "science_citations": 3},
        {"author": "Ivan_Drago", "science_citations": 1}
    ]

    for i, (actual_item, expected_item) in enumerate(zip(data, expected)):
        assert isinstance(actual_item, dict), f"Item at index {i} is not a JSON object."
        assert "author" in actual_item, f"Item at index {i} is missing the 'author' key."
        assert "science_citations" in actual_item, f"Item at index {i} is missing the 'science_citations' key."

        actual_author = actual_item["author"]
        actual_count = actual_item["science_citations"]

        expected_author = expected_item["author"]
        expected_count = expected_item["science_citations"]

        assert actual_author == expected_author, f"At rank {i+1}, expected author '{expected_author}' but got '{actual_author}'."
        assert actual_count == expected_count, f"At rank {i+1}, expected science_citations {expected_count} for '{actual_author}' but got {actual_count}."