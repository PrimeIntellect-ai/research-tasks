# test_final_state.py

import os
import pytest

def test_process_datasets_script_exists():
    path = "/home/user/process_datasets.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."

def test_processing_log_contents():
    path = "/home/user/processing.log"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    expected_lines = [
        "PROCESSED: dataset_alpha.tar.gz - EpiGen - L-101",
        "SKIPPED: dataset_malicious.tar.gz - ILLEGAL PATHS",
        "PROCESSED: dataset_gamma.tar.gz - Proteomics - L-303"
    ]

    for line in expected_lines:
        assert line in content, f"Expected log line '{line}' not found in {path}. Content:\n{content}"

def test_dataset_alpha_processed_correctly():
    path = "/home/user/organized/EpiGen/L-101/data1.tsv"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "PAT-REDACTED" in content, f"'PAT-REDACTED' not found in {path}."
    assert "PAT-1234" not in content, f"Unredacted ID 'PAT-1234' found in {path}."
    assert "PAT-5678" not in content, f"Unredacted ID 'PAT-5678' found in {path}."

def test_dataset_gamma_processed_correctly():
    path = "/home/user/organized/Proteomics/L-303/samples.tsv"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "PAT-REDACTED" in content, f"'PAT-REDACTED' not found in {path}."
    assert "PAT-9999" not in content, f"Unredacted ID 'PAT-9999' found in {path}."

def test_malicious_dataset_skipped():
    evil_path = "/tmp/evil.txt"
    assert not os.path.exists(evil_path), f"Malicious file {evil_path} was extracted!"

    organized_dir = "/home/user/organized/Transcriptomics"
    assert not os.path.exists(organized_dir), f"Directory {organized_dir} should not exist, as the dataset was malicious."