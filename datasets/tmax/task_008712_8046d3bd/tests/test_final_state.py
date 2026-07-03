# test_final_state.py
import os
import json

def test_top_triplets_json():
    json_path = "/home/user/top_triplets.json"
    assert os.path.exists(json_path), f"Output file missing at {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON"

    assert isinstance(data, list), "JSON root must be a list"
    assert len(data) == 3, f"Expected exactly 3 triplets, but found {len(data)}"

    expected_triplets = [
        {"A": 10, "B": 11, "C": 12},
        {"A": 30, "B": 31, "C": 32},
        {"A": 20, "B": 21, "C": 22}
    ]

    for i, expected in enumerate(expected_triplets):
        item = data[i]
        assert isinstance(item, dict), f"Item at index {i} is not a dictionary"

        for key in ["A", "B", "C", "score"]:
            assert key in item, f"Item at index {i} is missing key '{key}'"

        assert item["A"] == expected["A"], f"Expected A={expected['A']} at rank {i+1}, got {item['A']}"
        assert item["B"] == expected["B"], f"Expected B={expected['B']} at rank {i+1}, got {item['B']}"
        assert item["C"] == expected["C"], f"Expected C={expected['C']} at rank {i+1}, got {item['C']}"
        assert isinstance(item["score"], (int, float)), f"Score at rank {i+1} must be a number"

    # Check that scores are sorted in descending order
    scores = [item["score"] for item in data]
    assert scores == sorted(scores, reverse=True), "Scores are not sorted in descending order"