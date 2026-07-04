# test_final_state.py

import os
import pytest

def test_processed_log_1_skipped():
    """Ensure the file already in the manifest is skipped and not processed."""
    path = "/home/user/processed_logs/log_20231001_N01.csv"
    assert not os.path.exists(path), f"File {path} should not exist because it was already in the manifest."

def test_processed_log_2_exists_and_content():
    """Ensure the second log is processed correctly, encoded in UTF-8, and filtered."""
    path = "/home/user/processed_logs/log_20231002_N02.csv"
    assert os.path.isfile(path), f"File {path} does not exist."

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        pytest.fail(f"File {path} is not correctly encoded in UTF-8.")

    expected_lines = [
        "id,timestamp,status,message",
        "2,00:05,FAILED,Conexión falló en el servidor",
        "4,00:15,ERROR,Falló la operación"
    ]

    assert lines == expected_lines, f"Content of {path} does not match expected filtered output."

def test_processed_log_3_exists_and_content():
    """Ensure the third log is processed correctly, encoded in UTF-8, and filtered."""
    path = "/home/user/processed_logs/log_20231003_N03.csv"
    assert os.path.isfile(path), f"File {path} does not exist."

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except UnicodeDecodeError:
        pytest.fail(f"File {path} is not correctly encoded in UTF-8.")

    expected_lines = [
        "id,timestamp,status,message",
        "1,00:01,FAILED,Network timeout"
    ]

    assert lines == expected_lines, f"Content of {path} does not match expected filtered output."

def test_manifest_updated_correctly():
    """Ensure the manifest contains all the required files."""
    path = "/home/user/processed_manifest.txt"
    assert os.path.isfile(path), f"Manifest file {path} does not exist."

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_entries = {
        "log_20231001_N01.csv",
        "log_20231002_N02.csv",
        "log_20231003_N03.csv"
    }

    assert set(lines) == expected_entries, f"Manifest file content is incorrect. Expected entries: {expected_entries}, got: {set(lines)}"
    assert lines[0] == "log_20231001_N01.csv", "The first entry in the manifest should remain 'log_20231001_N01.csv'."
    assert len(lines) == 3, f"Manifest file should contain exactly 3 entries, but has {len(lines)}."