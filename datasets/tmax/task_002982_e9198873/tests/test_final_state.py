# test_final_state.py
import os
import json
import math

def test_summary_json_exists_and_correct():
    json_path = "/home/user/summary.json"
    assert os.path.isfile(json_path), f"File {json_path} is missing. Did you generate the output?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not a valid JSON file."

    assert isinstance(data, list), f"Expected the JSON root to be a list, got {type(data).__name__}."
    assert len(data) == 3, f"Expected 3 user objects in the JSON array, got {len(data)}."

    # Verify sorting by user_id
    user_ids = [obj.get("user_id") for obj in data]
    assert user_ids == ["U1", "U2", "U3"], f"Expected user_ids to be sorted ['U1', 'U2', 'U3'], got {user_ids}."

    expected_data = {
        "U1": {
            "total_spent": 415.5,
            "top_categories": ["Books", "Electronics"]
        },
        "U2": {
            "total_spent": 245.0,
            "top_categories": ["Clothing", "Home"]
        },
        "U3": {
            "total_spent": 300.0,
            "top_categories": ["Home"]
        }
    }

    for obj in data:
        user_id = obj.get("user_id")
        assert user_id in expected_data, f"Unexpected user_id: {user_id}"

        expected = expected_data[user_id]

        # Check total_spent
        total_spent = obj.get("total_spent")
        assert total_spent is not None, f"Missing 'total_spent' for user {user_id}"
        assert isinstance(total_spent, (int, float)), f"'total_spent' for user {user_id} should be a number."
        assert math.isclose(total_spent, expected["total_spent"], rel_tol=1e-5), \
            f"Expected total_spent for {user_id} to be {expected['total_spent']}, got {total_spent}."

        # Check top_categories
        top_categories = obj.get("top_categories")
        assert top_categories is not None, f"Missing 'top_categories' for user {user_id}"
        assert isinstance(top_categories, list), f"'top_categories' for user {user_id} should be a list."
        assert top_categories == expected["top_categories"], \
            f"Expected top_categories for {user_id} to be {expected['top_categories']}, got {top_categories}."

def test_cpp_files_exist():
    cpp_path = "/home/user/process_data.cpp"
    exe_path = "/home/user/process_data"

    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} is missing."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."