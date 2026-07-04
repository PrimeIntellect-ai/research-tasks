# test_final_state.py

import os
import tarfile
import pytest

def test_etl_output_file():
    """Check that the output summary file exists and contains the correct aggregated data."""
    output_path = '/home/user/etl_output/category_summary.tsv'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    expected_lines = [
        "Apparel\t232.50\t15.00",
        "Electronics\t1394.03\t104.95",
        "Groceries\t65.00\t0.00",
        "Home_Goods\t120.00\t30.00"
    ]

    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Content of {output_path} is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )

def test_archive_exists():
    """Check that the raw data archive was created and is a valid tar.gz file."""
    archive_path = '/home/user/archive/raw_data_backup.tar.gz'
    assert os.path.isfile(archive_path), f"Archive file {archive_path} does not exist."

    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, 'r:gz') as tar:
        names = tar.getnames()
        # Verify that it contains at least some of the expected files
        assert any("sales_20231001.csv" in name for name in names), "Archive does not contain the expected sales CSV files."

def test_raw_data_deleted():
    """Check that the original raw_data directory was deleted."""
    raw_data_path = '/home/user/raw_data/'
    assert not os.path.exists(raw_data_path), f"Directory {raw_data_path} still exists. It should have been deleted."