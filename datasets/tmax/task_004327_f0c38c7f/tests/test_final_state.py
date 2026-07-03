# test_final_state.py

import os
import csv
import math
import hashlib
import pytest

OUTPUT_CSV = "/home/user/pipeline/output.csv"
INPUT_CSV = "/home/user/data/input.csv"
HASH_TXT = "/home/user/pipeline/artifact_hash.txt"

def test_output_csv_exists():
    assert os.path.isfile(OUTPUT_CSV), f"Expected output file {OUTPUT_CSV} does not exist."

def test_output_csv_content():
    assert os.path.isfile(INPUT_CSV), f"Input file {INPUT_CSV} is missing."

    # Read input data
    input_data = []
    with open(INPUT_CSV, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            input_data.append((row["id"], float(row["sensor_value"])))

    # Compute expected statistics
    n = len(input_data)
    assert n > 0, "Input data is empty."

    mean = sum(val for _, val in input_data) / n
    variance = sum((val - mean) ** 2 for _, val in input_data) / n
    std_dev = math.sqrt(variance)

    # Read output data
    assert os.path.isfile(OUTPUT_CSV), f"Output file {OUTPUT_CSV} is missing."
    with open(OUTPUT_CSV, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["id", "sensor_value", "z_score"], f"Output CSV header is incorrect: {header}"

        output_rows = list(reader)

    assert len(output_rows) == n, f"Output CSV has {len(output_rows)} rows, expected {n}."

    for i, (expected_id, expected_val) in enumerate(input_data):
        out_id, out_val, out_z = output_rows[i]
        assert out_id == expected_id, f"Row {i+1}: expected id {expected_id}, got {out_id}"
        assert float(out_val) == expected_val, f"Row {i+1}: expected sensor_value {expected_val}, got {out_val}"

        expected_z = (expected_val - mean) / std_dev
        expected_z_str = f"{expected_z:.4f}"

        assert out_z == expected_z_str, f"Row {i+1}: expected z_score {expected_z_str}, got {out_z}"
        # Also check exact format (4 decimal places)
        assert len(out_z.split(".")[-1]) == 4, f"Row {i+1}: z_score {out_z} does not have exactly 4 decimal places."

def test_artifact_hash_exists_and_correct():
    assert os.path.isfile(OUTPUT_CSV), f"Output file {OUTPUT_CSV} is missing."
    assert os.path.isfile(HASH_TXT), f"Hash file {HASH_TXT} does not exist."

    with open(OUTPUT_CSV, "rb") as f:
        output_bytes = f.read()

    expected_hash = hashlib.sha256(output_bytes).hexdigest()

    with open(HASH_TXT, "r") as f:
        actual_hash_content = f.read().strip()

    # The file might contain just the hash, or "hash filename". We extract the first word.
    actual_hash = actual_hash_content.split()[0] if actual_hash_content else ""

    assert actual_hash == expected_hash, f"Hash mismatch. Expected {expected_hash}, got {actual_hash}."