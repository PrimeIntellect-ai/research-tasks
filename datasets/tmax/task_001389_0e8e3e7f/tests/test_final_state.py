# test_final_state.py

import os
import csv
import math
import pytest

def test_processed_csv_exists():
    processed_path = "/home/user/csv_processor/processed.csv"
    assert os.path.isfile(processed_path), f"Output file {processed_path} was not created."

def test_processed_csv_contents():
    input_path = "/home/user/csv_processor/dataset.csv"
    processed_path = "/home/user/csv_processor/processed.csv"

    # Read input to compute expected truth
    with open(input_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        input_rows = list(reader)

    train_rows = [r for r in input_rows if r['Split'] == 'train']

    # Compute mean
    n_train = len(train_rows)
    assert n_train > 1, "Need at least 2 train rows for sample stddev."

    mean_f1 = sum(float(r['F1']) for r in train_rows) / n_train
    mean_f2 = sum(float(r['F2']) for r in train_rows) / n_train
    mean_f3 = sum(float(r['F3']) for r in train_rows) / n_train

    # Compute sample stddev
    sq_diff_f1 = sum((float(r['F1']) - mean_f1) ** 2 for r in train_rows)
    sq_diff_f2 = sum((float(r['F2']) - mean_f2) ** 2 for r in train_rows)
    sq_diff_f3 = sum((float(r['F3']) - mean_f3) ** 2 for r in train_rows)

    std_f1 = math.sqrt(sq_diff_f1 / (n_train - 1))
    std_f2 = math.sqrt(sq_diff_f2 / (n_train - 1))
    std_f3 = math.sqrt(sq_diff_f3 / (n_train - 1))

    expected_output = []
    for r in input_rows:
        expected_output.append({
            'ID': r['ID'],
            'F1': f"{(float(r['F1']) - mean_f1) / std_f1:.4f}",
            'F2': f"{(float(r['F2']) - mean_f2) / std_f2:.4f}",
            'F3': f"{(float(r['F3']) - mean_f3) / std_f3:.4f}",
            'Split': r['Split']
        })

    # Read processed output
    with open(processed_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['ID', 'F1', 'F2', 'F3', 'Split'], f"Header is incorrect: {header}"

        output_rows = []
        for row in reader:
            output_rows.append({
                'ID': row[0],
                'F1': row[1],
                'F2': row[2],
                'F3': row[3],
                'Split': row[4]
            })

    assert len(output_rows) == len(expected_output), "Number of rows in processed.csv does not match dataset.csv."

    for i, (out_row, exp_row) in enumerate(zip(output_rows, expected_output)):
        assert out_row['ID'] == exp_row['ID'], f"Row {i+1} ID mismatch: expected {exp_row['ID']}, got {out_row['ID']}"
        assert out_row['Split'] == exp_row['Split'], f"Row {i+1} Split mismatch: expected {exp_row['Split']}, got {out_row['Split']}"
        assert out_row['F1'] == exp_row['F1'], f"Row {i+1} F1 mismatch: expected {exp_row['F1']}, got {out_row['F1']}"
        assert out_row['F2'] == exp_row['F2'], f"Row {i+1} F2 mismatch: expected {exp_row['F2']}, got {out_row['F2']}"
        assert out_row['F3'] == exp_row['F3'], f"Row {i+1} F3 mismatch: expected {exp_row['F3']}, got {out_row['F3']}"