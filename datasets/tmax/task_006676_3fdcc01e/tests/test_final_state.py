# test_final_state.py

import os
import random
import pytest

def test_sampled_data_exists_and_size():
    file_path = "/home/user/sampled_data.csv"
    assert os.path.isfile(file_path), f"Missing file: {file_path}. Did you run the compiled pipeline?"

    with open(file_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 51, f"Expected 51 lines in {file_path} (header + 50 rows), but got {len(lines)}."

    # Check header
    assert "id" in lines[0].lower(), "Header does not contain 'id'."

def test_sampled_data_content_and_determinism():
    file_path = "/home/user/sampled_data.csv"
    assert os.path.isfile(file_path), f"Missing file: {file_path}."

    with open(file_path, 'r') as f:
        lines = f.readlines()

    assert len(lines) == 51, "File does not have 51 lines."

    # Check that commas are present in the sampled rows (meaning join worked and commas are used)
    for i in range(1, 51):
        assert lines[i].count(',') >= 2, f"Row {i} does not appear to be properly comma-separated: {lines[i]}"

    # We need to verify the exact deterministic sequence.
    # The C++ mt19937 with seed 42, modulo 100.
    # Python's random uses MT19937, but its `random()` and `randrange()` methods do not map 1:1 to C++'s `gen() % 100`
    # because Python generates 53-bit floats or uses different logic for integers.
    # However, we can use a known sequence of C++ mt19937(42) % 100 for the first few values.
    # In C++, mt19937 with seed 42 generates:
    # 1st: 1608637542 % 100 = 42
    # 2nd: 3421126067 % 100 = 67
    # 3rd: 4083286876 % 100 = 76
    # 4th: 787228681 % 100 = 81
    # 5th: 3186930522 % 100 = 22
    # Note: The joined_data vector will have 100 elements. The indices are 0 to 99.
    # The IDs are 1 to 100.
    # If the map is used, iteration over the map or how it was inserted might affect order, but the code pushes to joined_data while iterating over embeddings.csv.
    # embeddings.csv has IDs 1 to 100 in order.
    # So joined_data[idx].id will be idx + 1.
    # Let's check the first few IDs.

    expected_indices = [42, 67, 76, 81, 22]
    expected_ids = [str(idx + 1) for idx in expected_indices]

    actual_ids = []
    for i in range(1, 6):
        parts = lines[i].split(',')
        actual_ids.append(parts[0])

    assert actual_ids == expected_ids, f"The sampled IDs do not match the expected deterministic sequence. Expected first 5 IDs: {expected_ids}, got: {actual_ids}. Did you use 'gen() % joined_data.size()' with seed 42?"

def test_pipeline_cpp_fixes():
    file_path = "/home/user/pipeline.cpp"
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, "r") as f:
        content = f.read()

    assert "std::random_device" not in content or "std::random_device rd;" not in content, "The code still uses std::random_device."
    assert "std::mt19937 gen(42);" in content or "gen(42)" in content, "The code does not initialize mt19937 with seed 42."
    assert "%" in content and "joined_data.size()" in content, "The code does not use modulo joined_data.size() for sampling."
    assert "std::uniform_int_distribution" not in content, "The code still uses std::uniform_int_distribution."
    assert "std::getline(ss, id, ',');" in content and "std::getline(ss, id, ' ');" not in content, "The delimiter for embeddings.csv was not fixed to a comma."