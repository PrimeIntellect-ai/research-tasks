# test_final_state.py
import os
import json
import pytest

def test_c_program_exists():
    assert os.path.isfile('/home/user/find_loops.c'), "The C program /home/user/find_loops.c does not exist."

def test_json_output_exists():
    assert os.path.isfile('/home/user/loops.json'), "The output file /home/user/loops.json does not exist."

def test_json_output_format_and_content():
    try:
        with open('/home/user/loops.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        pytest.fail(f"Failed to read or parse /home/user/loops.json: {e}")

    assert isinstance(data, list), "The JSON root must be an array."
    for item in data:
        assert isinstance(item, str), "All items in the JSON array must be strings."

    expected_loops = {
        "/home/user/dataset/loop_dir/child/grandchild/link_to_ancestor",
        "/home/user/dataset/mutualA/link_to_B",
        "/home/user/dataset/mutualB/link_to_A"
    }

    found_ancestor = "/home/user/dataset/loop_dir/child/grandchild/link_to_ancestor" in data
    found_mutual = ("/home/user/dataset/mutualA/link_to_B" in data) or ("/home/user/dataset/mutualB/link_to_A" in data)

    assert found_ancestor, "The ancestor loop symlink was not found in the output."
    assert found_mutual, "Neither of the mutual loop symlinks was found in the output."

    valid_links = [p for p in data if p not in expected_loops]
    assert len(valid_links) == 0, f"False positives found in the output: {valid_links}"