# test_final_state.py

import os
import pytest

def test_process_locales_script_exists_and_executable():
    """Check if the process_locales.sh script exists and is executable."""
    script_path = "/home/user/process_locales.sh"
    assert os.path.isfile(script_path), f"Script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_bulk_import_sql_exists():
    """Check if the bulk_import.sql file was generated."""
    sql_path = "/home/user/bulk_import.sql"
    assert os.path.isfile(sql_path), f"Output SQL file not found at {sql_path}"

def test_bulk_import_sql_content():
    """Check if the generated bulk_import.sql contains the correctly transformed data."""
    sql_path = "/home/user/bulk_import.sql"

    expected_lines = [
        "INSERT INTO locales (id, lang, txt, email) VALUES ('btn_ok', 'fr', 'D''accord', 'a***@example.com');",
        "INSERT INTO locales (id, lang, txt, email) VALUES ('msg_welcome', 'es', 'Hola,\\nbienvenido a nuestra app.', 'b***@translation.corp');",
        "INSERT INTO locales (id, lang, txt, email) VALUES ('err_404', 'de', 'Nicht gefunden.\\nBitte versuchen Sie es erneut.', 'c***@freelance.org');",
        "INSERT INTO locales (id, lang, txt, email) VALUES ('lbl_profile', 'ja', 'プロフィール', 'd***@tokyo.jp');",
        "INSERT INTO locales (id, lang, txt, email) VALUES ('msg_quote', 'en', 'It''s a \"\"quote\"\"', 'e***@test.com');"
    ]

    with open(sql_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip().splitlines()

    assert len(actual_content) == len(expected_lines), f"Expected {len(expected_lines)} lines in the output SQL, but got {len(actual_content)}."

    for i, (actual, expected) in enumerate(zip(actual_content, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"