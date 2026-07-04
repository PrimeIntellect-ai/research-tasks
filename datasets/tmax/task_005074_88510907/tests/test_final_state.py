# test_final_state.py

import os
import csv
import json
import math
import pytest

def compute_expected_features(input_path):
    expected = []
    if not os.path.exists(input_path):
        return expected

    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                id_val = int(row['ID'])
                vector_str = row['VectorData']
            except (KeyError, ValueError):
                continue

            # Replace Pi unicode escape with float string
            # Note: in Python, the string might be literally "\u03c0" or the actual unicode char
            vector_str = vector_str.replace('\\u03c0', '3.14159').replace('π', '3.14159')

            try:
                vector = json.loads(vector_str)
            except json.JSONDecodeError:
                continue

            if not isinstance(vector, list) or len(vector) < 3:
                continue

            try:
                vector = [float(x) for x in vector]
            except ValueError:
                continue

            # Compute L2 Norm
            l2_norm = math.sqrt(sum(x * x for x in vector))

            # Compute Population Variance
            mean = sum(vector) / len(vector)
            variance = sum((x - mean) ** 2 for x in vector) / len(vector)

            expected.append({
                'ID': id_val,
                'L2Norm': f"{l2_norm:.4f}",
                'Variance': f"{variance:.4f}"
            })

    # Sort by ID ascending
    expected.sort(key=lambda x: x['ID'])
    return expected

def test_go_source_exists():
    """Verify that the Go source file was created."""
    src_path = "/home/user/workspace/processor.go"
    assert os.path.isfile(src_path), f"Go source file is missing: {src_path}"

def test_output_file_exists():
    """Verify that the output CSV file was created."""
    out_path = "/home/user/data/features.csv"
    assert os.path.isfile(out_path), f"Output CSV file is missing: {out_path}"

def test_output_csv_content():
    """Verify the contents, formatting, and sorting of the output CSV."""
    in_path = "/home/user/data/raw_vectors.csv"
    out_path = "/home/user/data/features.csv"

    expected_data = compute_expected_features(in_path)

    with open(out_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("Output CSV is empty (missing header).")

        assert header == ['ID', 'L2Norm', 'Variance'], \
            f"CSV header is incorrect. Expected ['ID', 'L2Norm', 'Variance'], got {header}"

        actual_data = []
        for row in reader:
            if not row:
                continue
            assert len(row) == 3, f"Row does not have 3 columns: {row}"
            actual_data.append({
                'ID': int(row[0]),
                'L2Norm': row[1],
                'Variance': row[2]
            })

    assert len(actual_data) == len(expected_data), \
        f"Expected {len(expected_data)} valid rows, but found {len(actual_data)}."

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual['ID'] == expected['ID'], \
            f"Row {i+1}: Expected ID {expected['ID']}, got {actual['ID']} (Rows must be sorted by ID)"
        assert actual['L2Norm'] == expected['L2Norm'], \
            f"Row {i+1} (ID {actual['ID']}): Expected L2Norm {expected['L2Norm']}, got {actual['L2Norm']}"
        assert actual['Variance'] == expected['Variance'], \
            f"Row {i+1} (ID {actual['ID']}): Expected Variance {expected['Variance']}, got {actual['Variance']}"