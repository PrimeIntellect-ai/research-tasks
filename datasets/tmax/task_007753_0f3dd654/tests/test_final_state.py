# test_final_state.py

import os
import re

def test_extract_drops_cpp_exists():
    assert os.path.isfile('/home/user/extract_drops.cpp'), "The C++ source file /home/user/extract_drops.cpp does not exist."

def test_mmap_used_in_cpp():
    with open('/home/user/extract_drops.cpp', 'r') as f:
        content = f.read()
    assert re.search(r'\bmmap\s*\(', content), "The C++ program does not appear to use mmap() as required."

def test_dropped_objects_txt_exists():
    assert os.path.isfile('/home/user/dropped_objects.txt'), "The output file /home/user/dropped_objects.txt does not exist."

def test_dropped_objects_content():
    expected_ids = [12, 404, 777, 999]

    with open('/home/user/dropped_objects.txt', 'r') as f:
        lines = f.read().strip().split('\n')

    # Filter out any empty lines just in case
    lines = [line.strip() for line in lines if line.strip()]

    assert len(lines) == len(expected_ids), f"Expected {len(expected_ids)} unique DROP Object IDs, but found {len(lines)}."

    for i, expected_id in enumerate(expected_ids):
        try:
            actual_id = int(lines[i])
        except ValueError:
            assert False, f"Line {i+1} in dropped_objects.txt is not a valid integer: '{lines[i]}'."

        assert actual_id == expected_id, f"Expected Object ID {expected_id} at line {i+1}, but got {actual_id}. Ensure output is sorted and unique."