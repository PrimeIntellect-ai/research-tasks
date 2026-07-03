# test_final_state.py

import os
import json
import pytest

def test_hierarchy_json_exists_and_content():
    json_path = "/home/user/hierarchy.json"

    assert os.path.isfile(json_path), f"The file {json_path} was not created."

    expected_structure = [
        {
            "emp_id": "1",
            "name": "Alice",
            "subordinates": [
                {
                    "emp_id": "2",
                    "name": "Bob",
                    "subordinates": [
                        {
                            "emp_id": "4",
                            "name": "David",
                            "subordinates": [
                                {
                                    "emp_id": "7",
                                    "name": "Grace",
                                    "subordinates": []
                                }
                            ]
                        },
                        {
                            "emp_id": "5",
                            "name": "Eve",
                            "subordinates": []
                        }
                    ]
                },
                {
                    "emp_id": "3",
                    "name": "Charlie",
                    "subordinates": [
                        {
                            "emp_id": "6",
                            "name": "Frank",
                            "subordinates": []
                        }
                    ]
                }
            ]
        },
        {
            "emp_id": "8",
            "name": "Heidi",
            "subordinates": [
                {
                    "emp_id": "9",
                    "name": "Ivan",
                    "subordinates": []
                }
            ]
        }
    ]

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            actual_structure = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert actual_structure == expected_structure, f"The content of {json_path} does not match the expected hierarchical structure."