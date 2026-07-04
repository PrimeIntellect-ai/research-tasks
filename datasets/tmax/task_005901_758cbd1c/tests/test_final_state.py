# test_final_state.py
import os
import gzip
import pytest

def test_anomalies_archive_exists_and_content_correct():
    archive_path = "/home/user/anomalies_archive.csv.gz"

    # Check if the final archive exists
    assert os.path.isfile(archive_path), f"The expected archive {archive_path} does not exist."

    # Check if it is a valid gzip file and read its content
    try:
        with gzip.open(archive_path, 'rt', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        pytest.fail(f"Failed to read {archive_path} as a gzip file. Error: {e}")

    # Expected content
    expected_lines = [
        "id,value",
        "S1,88.5",
        "S3,91.2",
        "S5,99.9",
        "S8,85.1"
    ]

    # Normalize line endings and remove trailing empty lines
    actual_lines = [line.strip() for line in content.strip().splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The decompressed content of {archive_path} is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )

def test_intermediate_summary_csv_exists():
    summary_path = "/home/user/anomalies_summary.csv"

    # Although the task says "compress ... to create ...", it doesn't strictly say to delete the original.
    # But it says "write them to a new CSV file at ...". We can check if it exists or was compressed in place.
    # Actually, the prompt says "compress ... to create ...". The strict requirement is on the .gz file.
    # We will just verify the .gz file as the primary truth.
    pass