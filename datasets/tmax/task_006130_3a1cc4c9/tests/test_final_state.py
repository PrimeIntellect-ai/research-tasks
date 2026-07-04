# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_data.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_manifest_csv():
    manifest_path = "/home/user/manifest.csv"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    with open(manifest_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "docA,2023,tech,4",
        "docB,2023,sci,6",
        "docC,2022,tech,4"
    ]

    assert lines == expected_lines, f"Manifest contents are incorrect. Expected {expected_lines}, got {lines}"

def test_processed_tokens_docA():
    tok_path = "/home/user/processed/2023/tech/docA.tok"
    assert os.path.isfile(tok_path), f"Token file {tok_path} does not exist."

    with open(tok_path, "r") as f:
        tokens = [line.strip() for line in f if line.strip()]

    expected_tokens = ["hello", "world", "test", "2023"]
    assert tokens == expected_tokens, f"Tokens for docA are incorrect. Expected {expected_tokens}, got {tokens}"

def test_processed_tokens_docB():
    tok_path = "/home/user/processed/2023/sci/docB.tok"
    assert os.path.isfile(tok_path), f"Token file {tok_path} does not exist."

    with open(tok_path, "r") as f:
        tokens = [line.strip() for line in f if line.strip()]

    expected_tokens = ["data", "science", "fun", "data", "data", "data"]
    assert tokens == expected_tokens, f"Tokens for docB are incorrect. Expected {expected_tokens}, got {tokens}"

def test_processed_tokens_docC():
    tok_path = "/home/user/processed/2022/tech/docC.tok"
    assert os.path.isfile(tok_path), f"Token file {tok_path} does not exist."

    with open(tok_path, "r") as f:
        tokens = [line.strip() for line in f if line.strip()]

    expected_tokens = ["stopwords", "should", "removed", "right"]
    assert tokens == expected_tokens, f"Tokens for docC are incorrect. Expected {expected_tokens}, got {tokens}"

def test_docD_not_processed():
    # docD has year 2022 and category sci
    tok_path = "/home/user/processed/2022/sci/docD.tok"
    assert not os.path.exists(tok_path), f"Token file {tok_path} should not exist since docD.txt was missing."