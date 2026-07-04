# test_final_state.py

import os
import pytest

def test_recover_rs_exists():
    path = "/home/user/recover.rs"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

def test_cleaned_data_exists_and_clean():
    path = "/home/user/cleaned_data.bin"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

    with open(path, "rb") as f:
        data = f.read()

    poison_bytes = bytes([0xBA, 0xAD, 0xF0, 0x0D])
    assert poison_bytes not in data, "The cleaned_data.bin file still contains the poison bytes (0xBA 0xAD 0xF0 0x0D)."

    # Ensure the file size matches the original sensor_data.bin (144 bytes)
    assert len(data) == 144, f"Expected cleaned_data.bin to be 144 bytes, got {len(data)} bytes."

def test_report_txt_success():
    path = "/home/user/report.txt"
    assert os.path.exists(path), f"Missing file: {path}"
    assert os.path.isfile(path), f"Not a file: {path}"

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    expected_string = "SUCCESS: Processed 144 bytes, status converged."
    assert expected_string in content, f"The report.txt file does not contain the expected success message. Found: {content.strip()}"