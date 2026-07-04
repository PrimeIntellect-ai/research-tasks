# test_final_state.py

import os
import sqlite3
import math
import pytest

def test_invalid_strings_log():
    log_path = "/home/user/invalid_strings.log"
    assert os.path.exists(log_path), f"Log file {log_path} does not exist."

    expected_lines = [
        "1620000015,fr,invalid-key,Hello,Bonjour",
        "1620000020,de,welcome_msg,Welcome {user}!,Willkommen {name}!",
        "1620000030,BAD,test,test,test"
    ]

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_lines, f"Contents of {log_path} do not match the expected invalid rows."

def test_translations_db():
    db_path = "/home/user/translations.db"
    assert os.path.exists(db_path), f"Database file {db_path} does not exist."

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check schema
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='translations';")
    assert cursor.fetchone() is not None, "Table 'translations' does not exist in the database."

    # Check rows
    cursor.execute("SELECT lang_code, translation_key, original_text, translated_text, rolling_avg_ratio FROM translations ORDER BY lang_code DESC, translation_key DESC;")
    rows = cursor.fetchall()

    expected_rows = {
        ("fr", "welcome_msg"): ("Welcome {user}!", "Bienvenue cher {user}!", 1.28333333333333),
        ("fr", "goodbye"): ("Goodbye!", "Au revoir!", 1.19166666666666),
        ("es-ES", "welcome_msg"): ("Welcome {user}!", "Bienvenido {user}!", 1.2)
    }

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows in translations table, found {len(rows)}."

    for row in rows:
        lang_code, translation_key, original_text, translated_text, rolling_avg_ratio = row
        key = (lang_code, translation_key)
        assert key in expected_rows, f"Unexpected row found for {key}."

        expected_orig, expected_trans, expected_ratio = expected_rows[key]
        assert original_text == expected_orig, f"Expected original_text '{expected_orig}' for {key}, got '{original_text}'."
        assert translated_text == expected_trans, f"Expected translated_text '{expected_trans}' for {key}, got '{translated_text}'."
        assert math.isclose(rolling_avg_ratio, expected_ratio, rel_tol=1e-5), f"Expected rolling_avg_ratio ~{expected_ratio} for {key}, got {rolling_avg_ratio}."

    conn.close()