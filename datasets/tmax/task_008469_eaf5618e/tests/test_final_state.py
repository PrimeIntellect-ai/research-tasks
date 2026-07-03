# test_final_state.py

import os
import json
import stat

def test_schema_migrator_exists():
    path = "/home/user/schema_migrator.py"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_run_e2e_script_exists_and_executable():
    path = "/home/user/run_e2e.sh"
    assert os.path.exists(path), f"File {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

    # Check if executable
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_migrated_response_correct():
    response_path = "/home/user/migrated_response.json"
    assert os.path.exists(response_path), f"File {response_path} does not exist. Did the e2e script run successfully?"

    with open(response_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {response_path} does not contain valid JSON."

    # Derived expected state based on legacy_data.json
    expected_data = [
        {
            "first_name": "Alice",
            "last_name": "Walker",
            "age": 34,
            "identifier": 1
        },
        {
            "first_name": "Bob",
            "last_name": "Martin Lee",
            "age": 39,
            "identifier": 2
        }
    ]

    assert isinstance(data, list), "Migrated data should be a JSON array (list)."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual.get('first_name') == expected['first_name'], f"Item {i}: expected first_name '{expected['first_name']}', got '{actual.get('first_name')}'"
        assert actual.get('last_name') == expected['last_name'], f"Item {i}: expected last_name '{expected['last_name']}', got '{actual.get('last_name')}'"
        assert actual.get('age') == expected['age'], f"Item {i}: expected age {expected['age']}, got {actual.get('age')}"
        assert actual.get('identifier') == expected['identifier'], f"Item {i}: expected identifier {expected['identifier']}, got {actual.get('identifier')}"