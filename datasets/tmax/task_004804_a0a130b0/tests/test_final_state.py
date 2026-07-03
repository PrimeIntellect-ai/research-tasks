# test_final_state.py
import os
import csv
import json
import xml.etree.ElementTree as ET
import pytest

def compute_expected_diffs():
    xml_path = "/home/user/network_configs.xml"
    if not os.path.exists(xml_path):
        return []

    diffs = []
    prev_config = None

    # Simple parsing to extract just what we need to compute truth
    tree = ET.parse(xml_path)
    root = tree.getroot()
    for record in root.findall('record'):
        server_id = record.find('server_id').text
        if server_id != "core-router-01":
            continue

        timestamp = record.find('timestamp').text
        config_text = record.find('config').text
        current_config = json.loads(config_text)

        if prev_config is not None:
            current_diffs = []

            # Check for changed and removed keys
            for k, v in prev_config.items():
                if k not in current_config:
                    current_diffs.append((timestamp, k, str(v), "NONE"))
                elif current_config[k] != v:
                    current_diffs.append((timestamp, k, str(v), str(current_config[k])))

            # Check for added keys
            for k, v in current_config.items():
                if k not in prev_config:
                    current_diffs.append((timestamp, k, "NONE", str(v)))

            # Sort alphabetically by key name
            current_diffs.sort(key=lambda x: x[1])
            diffs.extend(current_diffs)

        prev_config = current_config

    return diffs

def test_diff_chunks_directory_exists():
    """Test that the output directory was created."""
    assert os.path.isdir("/home/user/diff_chunks"), "Directory /home/user/diff_chunks/ was not created."

def test_chunked_files_content():
    """Test that the chunked CSV files exist and contain the correct diffs."""
    expected_diffs = compute_expected_diffs()
    assert len(expected_diffs) > 0, "No diffs computed from the input file."

    chunk_size = 20
    expected_chunks = [expected_diffs[i:i + chunk_size] for i in range(0, len(expected_diffs), chunk_size)]

    for i, chunk in enumerate(expected_chunks, start=1):
        file_path = f"/home/user/diff_chunks/core_router_diffs_part{i}.csv"
        assert os.path.exists(file_path), f"Expected chunk file {file_path} is missing."

        with open(file_path, "r", newline="") as f:
            reader = csv.reader(f)
            rows = list(reader)

        assert len(rows) > 0, f"File {file_path} is empty."
        assert rows[0] == ["timestamp", "key", "old_value", "new_value"], f"Header in {file_path} is incorrect."

        data_rows = rows[1:]
        assert len(data_rows) == len(chunk), f"File {file_path} has {len(data_rows)} records, expected {len(chunk)}."

        for row_idx, (actual, expected) in enumerate(zip(data_rows, chunk)):
            assert tuple(actual) == expected, f"Mismatch in {file_path} at row {row_idx + 2}. Expected {expected}, got {tuple(actual)}."

def test_no_extra_files():
    """Test that there are no extra unexpected files in the chunks directory."""
    expected_diffs = compute_expected_diffs()
    num_chunks = (len(expected_diffs) + 19) // 20

    expected_files = {f"core_router_diffs_part{i}.csv" for i in range(1, num_chunks + 1)}

    if os.path.isdir("/home/user/diff_chunks"):
        actual_files = set(os.listdir("/home/user/diff_chunks"))
        extra_files = actual_files - expected_files
        assert not extra_files, f"Found unexpected files in /home/user/diff_chunks/: {extra_files}"