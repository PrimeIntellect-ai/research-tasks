# test_final_state.py

import os
import json
import pytest

def test_deployment_plan_exists_and_valid():
    path = "/home/user/deployment_plan.json"
    assert os.path.isfile(path), f"Missing file: {path}. The Rust program must generate this file."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"File {path} is not valid JSON. Error: {e}")

    assert "actions" in data, f"The JSON in {path} must contain an 'actions' key at the top level."
    actions = data["actions"]
    assert isinstance(actions, list), f"The 'actions' key must be a list, found {type(actions)}."
    assert len(actions) == 5, f"Expected exactly 5 actions, found {len(actions)}."

    expected_actions = [
        {
            "action": "UPGRADE",
            "name": "auth-api",
            "from_version": "2.1.0",
            "to_version": "2.2.0"
        },
        {
            "action": "REMOVE",
            "name": "notification-svc",
            "from_version": "1.1.0",
            "to_version": None
        },
        {
            "action": "KEEP",
            "name": "payment-gateway",
            "from_version": "1.0.5",
            "to_version": "1.0.5"
        },
        {
            "action": "INSTALL",
            "name": "search-indexer",
            "from_version": None,
            "to_version": "0.9.0"
        },
        {
            "action": "ROLLBACK",
            "name": "user-db",
            "from_version": "3.0.0-beta.2",
            "to_version": "3.0.0-beta.1"
        }
    ]

    # Check order
    actual_names = [a.get("name") for a in actions]
    expected_names = [a["name"] for a in expected_actions]
    assert actual_names == expected_names, f"Actions are not sorted alphabetically by name or missing names. Expected {expected_names}, got {actual_names}."

    # Check exact contents
    for i, (actual, expected) in enumerate(zip(actions, expected_actions)):
        name = expected["name"]

        # Action
        assert actual.get("action") == expected["action"], f"For service '{name}', expected action '{expected['action']}', got '{actual.get('action')}'."

        # from_version
        assert actual.get("from_version") == expected["from_version"], f"For service '{name}', expected from_version '{expected['from_version']}', got '{actual.get('from_version')}'."

        # to_version
        assert actual.get("to_version") == expected["to_version"], f"For service '{name}', expected to_version '{expected['to_version']}', got '{actual.get('to_version')}'."