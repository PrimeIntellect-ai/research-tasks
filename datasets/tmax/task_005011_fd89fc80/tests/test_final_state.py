# test_final_state.py
import os
import json
import pytest

def test_network_json_output():
    json_path = '/home/user/network_1.json'
    assert os.path.isfile(json_path), f"Expected JSON file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    assert "target_author" in data, "JSON missing 'target_author' key."
    assert data["target_author"] == 1, f"Expected target_author to be 1, got {data['target_author']}."

    assert "network" in data, "JSON missing 'network' key."
    network = data["network"]
    assert isinstance(network, list), "'network' should be a list."

    expected_network = [
        { "author_id": 2, "name": "Bob", "distance": 1, "wikidata_q": "Q222" },
        { "author_id": 5, "name": "Eve", "distance": 1, "wikidata_q": "Q555" },
        { "author_id": 3, "name": "Charlie", "distance": 2, "wikidata_q": "Q333" }
    ]

    assert len(network) == len(expected_network), f"Expected {len(expected_network)} authors in network, got {len(network)}."

    for i, expected_author in enumerate(expected_network):
        actual_author = network[i]
        assert actual_author.get("author_id") == expected_author["author_id"], f"Expected author_id {expected_author['author_id']} at index {i}, got {actual_author.get('author_id')}."
        assert actual_author.get("name") == expected_author["name"], f"Expected name '{expected_author['name']}' at index {i}, got '{actual_author.get('name')}'."
        assert actual_author.get("distance") == expected_author["distance"], f"Expected distance {expected_author['distance']} at index {i}, got {actual_author.get('distance')}."
        assert actual_author.get("wikidata_q") == expected_author["wikidata_q"], f"Expected wikidata_q '{expected_author['wikidata_q']}' at index {i}, got '{actual_author.get('wikidata_q')}'."

def test_wikidata_rq_output():
    rq_path = '/home/user/wikidata_1.rq'
    assert os.path.isfile(rq_path), f"Expected SPARQL file {rq_path} does not exist."

    with open(rq_path, 'r') as f:
        content = f.read()

    # Check for VALUES clause and expected Wikidata IDs
    assert "VALUES" in content.upper(), "SPARQL query missing VALUES clause."

    expected_q_ids = ["wd:Q222", "wd:Q333", "wd:Q555"]
    for q_id in expected_q_ids:
        assert q_id in content, f"SPARQL query missing expected Wikidata ID {q_id}."

    # Check for variables
    expected_vars = ["?author", "?dob", "?employer"]
    for var in expected_vars:
        assert var in content, f"SPARQL query missing expected variable {var}."

    # Check for properties
    expected_props = ["wdt:P569", "wdt:P108"]
    for prop in expected_props:
        assert prop in content, f"SPARQL query missing expected property {prop}."