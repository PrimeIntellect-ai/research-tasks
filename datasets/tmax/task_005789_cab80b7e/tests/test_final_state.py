# test_final_state.py

import os
import json
import csv
import pytest

def test_processed_metrics_csv():
    file_path = "/home/user/processed_metrics.csv"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    # Compute expected values
    raw_data = [
        (1, 45.0, 60.0, 120.0, 15.2),
        (2, 85.0, 90.0, 80.0, 45.5),
        (3, 20.0, 30.0, 200.0, 5.0),
        (4, 95.0, 88.0, 50.0, 80.1),
        (5, 50.0, 50.0, 150.0, 20.0),
        (6, 70.0, 75.0, 100.0, 35.4),
        (7, 10.0, 20.0, 250.0, 2.1),
        (8, 65.0, 70.0, 110.0, 28.9),
        (9, 90.0, 85.0, 60.0, 65.2),
        (10, 35.0, 40.0, 180.0, 10.5)
    ]

    cpu_min, cpu_max = 10.0, 95.0
    mem_min, mem_max = 20.0, 90.0
    disk_min, disk_max = 50.0, 250.0

    load_indices = [(cpu * mem) / disk for _, cpu, mem, disk, _ in raw_data]
    li_min, li_max = min(load_indices), max(load_indices)

    expected_rows = []
    for i, row in enumerate(raw_data):
        id_val, cpu, mem, disk, latency = row
        li = load_indices[i]

        cpu_scaled = (cpu - cpu_min) / (cpu_max - cpu_min)
        mem_scaled = (mem - mem_min) / (mem_max - mem_min)
        disk_scaled = (disk - disk_min) / (disk_max - disk_min)
        li_scaled = (li - li_min) / (li_max - li_min)

        expected_rows.append([
            str(id_val),
            f"{cpu_scaled:.4f}",
            f"{mem_scaled:.4f}",
            f"{disk_scaled:.4f}",
            f"{li_scaled:.4f}",
            f"{latency:.4f}" if isinstance(latency, float) else str(latency)
        ])

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        expected_header = ["ID", "CPU_scaled", "Memory_scaled", "DiskIO_scaled", "LoadIndex_scaled", "Latency"]
        assert [h.strip() for h in header] == expected_header, "CSV header is incorrect."

        actual_rows = list(reader)
        assert len(actual_rows) == len(expected_rows), "Incorrect number of rows in processed_metrics.csv."

        for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
            # ID and Latency might not be exactly 4 decimal places depending on how it was printed, 
            # but the prompt says "All float values should be formatted to 4 decimal places."
            # So we strictly check 4 decimal places for all floats.
            assert actual[0] == expected[0], f"Row {i+1} ID mismatch: expected {expected[0]}, got {actual[0]}"
            assert actual[1] == expected[1], f"Row {i+1} CPU_scaled mismatch: expected {expected[1]}, got {actual[1]}"
            assert actual[2] == expected[2], f"Row {i+1} Memory_scaled mismatch: expected {expected[2]}, got {actual[2]}"
            assert actual[3] == expected[3], f"Row {i+1} DiskIO_scaled mismatch: expected {expected[3]}, got {actual[3]}"
            assert actual[4] == expected[4], f"Row {i+1} LoadIndex_scaled mismatch: expected {expected[4]}, got {actual[4]}"

            # Latency check: allow both original string or 4 decimal places
            actual_lat = float(actual[5])
            expected_lat = float(expected[5])
            assert abs(actual_lat - expected_lat) < 1e-4, f"Row {i+1} Latency mismatch: expected {expected[5]}, got {actual[5]}"

def test_bootstrap_means_json():
    file_path = "/home/user/bootstrap_means.json"
    assert os.path.exists(file_path), f"Output file {file_path} is missing."

    with open(file_path, "r") as f:
        try:
            means = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {file_path} is not valid JSON.")

    assert isinstance(means, list), "JSON output should be a list."
    assert len(means) == 5, "JSON output should contain exactly 5 means."

    # Expected values derived from Go 1.20+ math/rand with seed 12345
    expected_means = [36.82, 19.01, 18.99, 29.50, 15.90]

    for i, (actual, expected) in enumerate(zip(means, expected_means)):
        assert isinstance(actual, (int, float)), f"Mean at index {i} is not a number."
        assert abs(actual - expected) < 1e-2, f"Bootstrap mean {i+1} mismatch: expected ~{expected}, got {actual}"