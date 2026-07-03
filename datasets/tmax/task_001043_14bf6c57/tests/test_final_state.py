# test_final_state.py

import os
import json
import pytest

FINAL_BOM_PATH = "/home/user/final_bom.json"

EXPECTED_BOM = [
    {
        "category": "Fastener",
        "is_leaf": True,
        "name": "Screws",
        "part_id": "PART-100"
    },
    {
        "category": "Electrical",
        "is_leaf": True,
        "name": "DC Motor",
        "part_id": "PART-200"
    },
    {
        "category": "Housing",
        "is_leaf": True,
        "name": "Plastic Shell",
        "part_id": "PART-300"
    },
    {
        "category": "Accessory",
        "is_leaf": True,
        "name": "Rubber Feet",
        "part_id": "PART-400"
    },
    {
        "category": "Subassembly",
        "is_leaf": False,
        "name": "Motor Assembly",
        "part_id": "SUB-010"
    },
    {
        "category": "Subassembly",
        "is_leaf": False,
        "name": "Casing Assembly",
        "part_id": "SUB-020"
    }
]

def test_final_bom_exists():
    assert os.path.isfile(FINAL_BOM_PATH), f"Output file {FINAL_BOM_PATH} does not exist."

def test_final_bom_format_and_content():
    with open(FINAL_BOM_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {FINAL_BOM_PATH} is not valid JSON.")

    assert isinstance(data, list), f"Expected JSON root to be a list, got {type(data).__name__}."

    # Check sorting
    part_ids = [item.get("part_id") for item in data if isinstance(item, dict)]
    assert part_ids == sorted(part_ids), "The JSON array is not sorted alphabetically by part_id."

    # Check length
    assert len(data) == len(EXPECTED_BOM), f"Expected {len(EXPECTED_BOM)} items, found {len(data)}."

    # Check exact content
    for expected_item, actual_item in zip(EXPECTED_BOM, data):
        assert isinstance(actual_item, dict), "Each item in the JSON array must be an object/dictionary."

        for key in ["part_id", "name", "category", "is_leaf"]:
            assert key in actual_item, f"Missing key '{key}' in item {actual_item}"
            assert actual_item[key] == expected_item[key], (
                f"Mismatch for part_id {expected_item['part_id']} on key '{key}': "
                f"expected {expected_item[key]}, got {actual_item[key]}"
            )

        # Ensure no extra keys
        extra_keys = set(actual_item.keys()) - set(expected_item.keys())
        assert not extra_keys, f"Found unexpected keys in item {actual_item['part_id']}: {extra_keys}"