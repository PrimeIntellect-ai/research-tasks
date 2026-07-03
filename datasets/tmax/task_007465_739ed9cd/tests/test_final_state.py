# test_final_state.py

import os
import sqlite3
import pytest

def test_v2_db_exists_and_correct():
    v1_db_path = "/home/user/mobile_build/data/v1.db"
    v2_db_path = "/home/user/mobile_build/data/v2.db"

    assert os.path.isfile(v1_db_path), f"Original v1.db is missing at {v1_db_path}."
    assert os.path.isfile(v2_db_path), f"Migrated v2.db is missing at {v2_db_path}."

    # Read v1.db to compute expected values
    conn1 = sqlite3.connect(v1_db_path)
    cursor1 = conn1.cursor()
    cursor1.execute("SELECT id, ts, val FROM raw_metrics ORDER BY ts ASC;")
    v1_rows = cursor1.fetchall()
    conn1.close()

    expected_v2_rows = []
    alpha = 0.25
    current_ema = None
    for row in v1_rows:
        row_id, ts, val = row
        if current_ema is None:
            current_ema = val
        else:
            current_ema = (val * alpha) + (current_ema * (1 - alpha))
        expected_v2_rows.append((row_id, ts, val, current_ema))

    # Read v2.db and verify
    conn2 = sqlite3.connect(v2_db_path)
    cursor2 = conn2.cursor()

    cursor2.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metrics_v2';")
    assert cursor2.fetchone() is not None, "Table 'metrics_v2' does not exist in v2.db."

    cursor2.execute("SELECT id, ts, val, ema FROM metrics_v2 ORDER BY ts ASC;")
    v2_rows = cursor2.fetchall()
    conn2.close()

    assert len(v2_rows) == len(expected_v2_rows), f"Expected {len(expected_v2_rows)} rows in metrics_v2, found {len(v2_rows)}."

    for actual, expected in zip(v2_rows, expected_v2_rows):
        assert actual[0] == expected[0], f"ID mismatch: expected {expected[0]}, got {actual[0]}"
        assert actual[1] == expected[1], f"TS mismatch: expected {expected[1]}, got {actual[1]}"
        assert actual[2] == expected[2], f"VAL mismatch: expected {expected[2]}, got {actual[2]}"
        # Allow small floating point differences
        assert abs(actual[3] - expected[3]) < 1e-6, f"EMA mismatch at id {actual[0]}: expected {expected[3]}, got {actual[3]}"

def test_signature_artifact_exists_and_valid():
    v2_db_path = "/home/user/mobile_build/data/v2.db"
    sig_path = "/home/user/mobile_build/data/v2.db.sig"

    assert os.path.isfile(v2_db_path), "v2.db is missing, cannot verify signature."
    assert os.path.isfile(sig_path), f"Signature file is missing at {sig_path}."

    with open(v2_db_path, 'rb') as f:
        db_content = f.read()

    # Compute expected hash (wrapping sum of bytes as u32)
    expected_hash = sum(db_content) % (2**32)

    with open(sig_path, 'r') as f:
        sig_content = f.read().strip().split('\n')

    assert len(sig_content) >= 3, "Signature file does not have the expected number of lines."

    label_line = sig_content[0]
    msg_line = sig_content[1]
    hash_line = sig_content[2]

    assert label_line == "LABEL:SIGNED_FILE_", f"Incorrect label line: {label_line}"
    assert msg_line == f"MSG:SIGNED_FILE_{v2_db_path}", f"Incorrect msg line: {msg_line}"
    assert hash_line == f"HASH:{expected_hash}", f"Incorrect hash line: expected HASH:{expected_hash}, got {hash_line}"

def test_rust_tool_compiled():
    tool_executable = "/home/user/mobile_build/tools/db_signer/target/release/db_signer"
    assert os.path.isfile(tool_executable), f"Compiled Rust tool missing at {tool_executable}. Did you run 'cargo build --release'?"
    assert os.access(tool_executable, os.X_OK), f"The tool at {tool_executable} is not executable."