# test_final_state.py
import os
import csv
import re
import pytest

def compute_expected_output(input_path):
    expected_rows = [['category', 'normalized_text', 'token_count', 'rolling_avg']]
    category_counts = {}
    category_prev_tokens = {}

    with open(input_path, 'r') as f:
        for line in f:
            if not line.strip("\n"):
                continue
            parts = line.strip("\n").split('\t')
            if len(parts) != 2:
                continue
            category, raw_text = parts

            if category_counts.get(category, 0) >= 3:
                continue

            # Normalize
            normalized = re.sub(r'[^a-z0-9 ]', '', raw_text.lower())
            tokens = [t for t in normalized.split(' ') if t]
            normalized_text = ' '.join(tokens)
            token_count = len(tokens)

            # Rolling avg
            if category not in category_prev_tokens:
                rolling_avg = float(token_count)
            else:
                rolling_avg = (token_count + category_prev_tokens[category]) / 2.0

            category_prev_tokens[category] = token_count
            category_counts[category] = category_counts.get(category, 0) + 1

            expected_rows.append([category, normalized_text, str(token_count), f"{rolling_avg:.1f}"])

    return expected_rows

def test_output_csv_exists_and_correct():
    input_file = "/home/user/input.tsv"
    output_file = "/home/user/output.csv"

    assert os.path.exists(input_file), f"Input file {input_file} is missing."
    assert os.path.exists(output_file), f"Output file {output_file} was not created."

    expected_data = compute_expected_output(input_file)

    with open(output_file, 'r') as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, "Output CSV is empty."
    assert reader[0] == expected_data[0], f"CSV headers do not match. Expected {expected_data[0]}, got {reader[0]}"

    assert len(reader) == len(expected_data), f"Output CSV has incorrect number of rows. Expected {len(expected_data)}, got {len(reader)}"

    for i, (actual, expected) in enumerate(zip(reader, expected_data)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}"