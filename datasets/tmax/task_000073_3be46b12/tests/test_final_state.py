# test_final_state.py

import os
import csv
import pytest

def test_pca_components_file():
    filepath = "/home/user/pca_components.txt"
    assert os.path.isfile(filepath), f"File not found: {filepath}"

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"Expected an integer in {filepath}, got: {content}"
    assert int(content) > 0, "PCA components must be greater than 0"

def test_removed_ids_file():
    filepath = "/home/user/removed_ids.txt"
    assert os.path.isfile(filepath), f"File not found: {filepath}"

    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    removed_ids = []
    for line in lines:
        assert line.lstrip('-').isdigit(), f"Expected integer ID, got: {line}"
        removed_ids.append(int(line))

    # Check if sorted in ascending order
    assert removed_ids == sorted(removed_ids), "Removed IDs are not sorted in ascending order"

def test_cleaned_embeddings_and_partition():
    orig_filepath = "/home/user/data/embeddings.csv"
    cleaned_filepath = "/home/user/cleaned_embeddings.csv"
    removed_filepath = "/home/user/removed_ids.txt"

    assert os.path.isfile(orig_filepath), f"Original data not found: {orig_filepath}"
    assert os.path.isfile(cleaned_filepath), f"Cleaned data not found: {cleaned_filepath}"
    assert os.path.isfile(removed_filepath), f"Removed IDs file not found: {removed_filepath}"

    # Read original data
    orig_data = {}
    with open(orig_filepath, "r", newline="") as f:
        reader = csv.reader(f)
        orig_header = next(reader)
        for row in reader:
            orig_data[int(row[0])] = row

    # Read removed IDs
    with open(removed_filepath, "r") as f:
        removed_ids = set(int(line.strip()) for line in f if line.strip())

    # Read cleaned data
    cleaned_ids = []
    cleaned_data = {}
    with open(cleaned_filepath, "r", newline="") as f:
        reader = csv.reader(f)
        cleaned_header = next(reader)
        assert cleaned_header == orig_header, "Header in cleaned dataset does not match original"

        for row in reader:
            row_id = int(row[0])
            cleaned_ids.append(row_id)
            cleaned_data[row_id] = row

    # Check sorting of cleaned data
    assert cleaned_ids == sorted(cleaned_ids), "Cleaned dataset is not sorted by id in ascending order"

    # Check partition property: original IDs = cleaned IDs + removed IDs
    orig_id_set = set(orig_data.keys())
    cleaned_id_set = set(cleaned_ids)

    assert cleaned_id_set.isdisjoint(removed_ids), "Cleaned dataset contains IDs that were marked for removal"
    assert orig_id_set == cleaned_id_set.union(removed_ids), "Cleaned IDs and removed IDs do not exactly partition the original IDs"

    # Check data integrity: cleaned rows must exactly match original rows
    for cid in cleaned_ids:
        assert cleaned_data[cid] == orig_data[cid], f"Data for id {cid} was altered in the cleaned dataset"