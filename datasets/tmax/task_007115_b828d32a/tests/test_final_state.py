# test_final_state.py

import os
import tarfile
import csv
import pytest

def test_high_intensity_csv_exists_and_content():
    """Test that high_intensity.csv exists and contains the correct filtered data."""
    csv_path = '/home/user/high_intensity.csv'
    assert os.path.exists(csv_path), f"The file {csv_path} does not exist."
    assert os.path.isfile(csv_path), f"The path {csv_path} is not a file."

    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"The file {csv_path} is empty."

    header = rows[0]
    expected_header = ['id', 'timestamp', 'intensity', 'wavelength']
    assert header == expected_header, f"Header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    expected_data = [
        ['2', '1005', '150', '405'],
        ['3', '1010', '200', '410'],
        ['7', '1030', '110', '430']
    ]

    # Sort both to allow any order
    data_rows_sorted = sorted(data_rows)
    expected_data_sorted = sorted(expected_data)

    assert data_rows_sorted == expected_data_sorted, f"Data rows do not match expected filtered data. Got {data_rows_sorted}"

def test_processed_archive_exists_and_contents():
    """Test that processed_spectroscopy.tar.gz exists and contains exactly the required files."""
    archive_path = '/home/user/processed_spectroscopy.tar.gz'
    assert os.path.exists(archive_path), f"The archive {archive_path} does not exist."
    assert os.path.isfile(archive_path), f"The path {archive_path} is not a file."
    assert tarfile.is_tarfile(archive_path), f"The file {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, 'r:gz') as tar:
        members = tar.getmembers()

    # Extract file paths, ignoring directories
    file_paths = [m.name for m in members if m.isfile()]

    # Normalize paths (remove leading './' if present)
    normalized_paths = set()
    for p in file_paths:
        if p.startswith('./'):
            normalized_paths.add(p[2:])
        else:
            normalized_paths.add(p)

    expected_files = {
        'high_intensity.csv',
        'exp_001/meta.json',
        'exp_004/meta.json'
    }

    assert normalized_paths == expected_files, f"Archive contents do not match expected. Expected {expected_files}, got {normalized_paths}."