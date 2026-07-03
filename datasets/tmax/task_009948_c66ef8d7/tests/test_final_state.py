# test_final_state.py

import os
import json
import hashlib
import pytest

RAW_DIR = "/home/user/raw_logs"
OUT_DIR = "/home/user/processed_logs"
MANIFEST_PATH = os.path.join(OUT_DIR, "manifest.json")

def get_file_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def extract_transactions(content):
    transactions = []
    current_tx = []
    in_tx = False
    for line in content.splitlines(keepends=True):
        if line.startswith("=== START TRANSACTION"):
            in_tx = True
            current_tx = [line]
        elif line.startswith("=== END TRANSACTION"):
            if in_tx:
                current_tx.append(line)
                transactions.append("".join(current_tx))
                in_tx = False
        elif in_tx:
            current_tx.append(line)
    return transactions

def test_processed_logs_dir_exists():
    assert os.path.exists(OUT_DIR), f"Output directory {OUT_DIR} does not exist."
    assert os.path.isdir(OUT_DIR), f"{OUT_DIR} is not a directory."

def test_no_tmp_files():
    assert os.path.exists(OUT_DIR), f"Output directory {OUT_DIR} does not exist."
    for fname in os.listdir(OUT_DIR):
        assert not fname.endswith(".tmp"), f"Temporary file {fname} found in {OUT_DIR}."

def test_node1_log_content():
    processed_node1 = os.path.join(OUT_DIR, "node1.log")
    assert os.path.exists(processed_node1), f"Processed file {processed_node1} does not exist."

    with open(processed_node1, "r") as f:
        content = f.read()

    transactions = extract_transactions(content)
    assert len(transactions) == 1, f"Expected exactly 1 transaction in node1.log, found {len(transactions)}."
    assert "=== START TRANSACTION 102 ===" in transactions[0], "Transaction 102 is missing in node1.log."
    assert "Status: FAILED" in transactions[0], "Transaction 102 should have Status: FAILED."
    assert "=== START TRANSACTION 101 ===" not in content, "Transaction 101 (SUCCESS) should not be in node1.log."
    assert "=== START TRANSACTION 103 ===" not in content, "Transaction 103 (SUCCESS) should not be in node1.log."

def test_node2_log_content():
    processed_node2 = os.path.join(OUT_DIR, "node2.log")
    assert os.path.exists(processed_node2), f"Processed file {processed_node2} does not exist."

    with open(processed_node2, "r") as f:
        content = f.read()

    transactions = extract_transactions(content)
    assert len(transactions) == 2, f"Expected exactly 2 transactions in node2.log, found {len(transactions)}."

    tx_ids = []
    for tx in transactions:
        if "=== START TRANSACTION 201 ===" in tx:
            tx_ids.append(201)
        elif "=== START TRANSACTION 202 ===" in tx:
            tx_ids.append(202)

    assert 201 in tx_ids, "Transaction 201 is missing in node2.log."
    assert 202 in tx_ids, "Transaction 202 is missing in node2.log."

def test_manifest_exists_and_valid():
    assert os.path.exists(MANIFEST_PATH), f"Manifest file {MANIFEST_PATH} does not exist."

    with open(MANIFEST_PATH, "r") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Manifest file {MANIFEST_PATH} is not valid JSON.")

    assert isinstance(manifest, dict), "Manifest JSON should be a dictionary."

    expected_files = ["node1.log", "node2.log"]
    for fname in expected_files:
        assert fname in manifest, f"File {fname} is missing from the manifest."

        filepath = os.path.join(OUT_DIR, fname)
        assert os.path.exists(filepath), f"File {fname} listed in manifest does not exist in {OUT_DIR}."

        actual_hash = get_file_sha256(filepath)
        assert manifest[fname] == actual_hash, f"SHA256 hash mismatch for {fname}. Expected {actual_hash}, got {manifest[fname]}."