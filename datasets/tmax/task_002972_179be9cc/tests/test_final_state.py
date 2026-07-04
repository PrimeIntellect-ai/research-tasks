# test_final_state.py

import os
import csv
import pytest

def test_joined_data_exists_and_format():
    """Test that joined_data.csv exists, has the correct header, and correct row count."""
    file_path = "/home/user/joined_data.csv"
    assert os.path.isfile(file_path), f"Missing {file_path}"

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, f"{file_path} is empty"
        assert "id" in header, f"'id' column missing in {file_path}"

        rows = list(reader)
        # 100 total ids, dfB misses 10, dfC misses 10 (different ones or same ones? The setup says ids[:90] and ids[10:], so intersection is ids[10:90] which is 80 ids)
        assert len(rows) == 80, f"Expected 80 data rows in {file_path}, found {len(rows)}"

def test_pca_python_exists_and_format():
    """Test that pca_python.csv exists and has correct dimensions."""
    file_path = "/home/user/pca_python.csv"
    assert os.path.isfile(file_path), f"Missing {file_path}"

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, f"{file_path} is empty"
        assert header == ["PC1", "PC2"], f"Header in {file_path} should be exactly ['PC1', 'PC2']"

        rows = list(reader)
        assert len(rows) == 80, f"Expected 80 data rows in {file_path}, found {len(rows)}"

def test_pca_r_exists_and_format():
    """Test that pca_r.csv exists and has correct dimensions."""
    file_path = "/home/user/pca_r.csv"
    assert os.path.isfile(file_path), f"Missing {file_path}"

    with open(file_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header is not None, f"{file_path} is empty"

        # R might quote the headers, but csv reader should handle standard quoting.
        # Just check the names.
        assert header == ["PC1", "PC2"], f"Header in {file_path} should be exactly ['PC1', 'PC2']"

        rows = list(reader)
        assert len(rows) == 80, f"Expected 80 data rows in {file_path}, found {len(rows)}"

def test_accuracy_report():
    """Test that accuracy_report.txt exists and contains PASS."""
    file_path = "/home/user/accuracy_report.txt"
    assert os.path.isfile(file_path), f"Missing {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "PASS", f"Expected 'PASS' in {file_path}, found '{content}'"

def test_pipeline_script_exists():
    """Test that run_pipeline.sh exists."""
    file_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(file_path), f"Missing pipeline script {file_path}"