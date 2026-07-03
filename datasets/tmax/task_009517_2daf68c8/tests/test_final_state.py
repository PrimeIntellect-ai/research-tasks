# test_final_state.py

import os
import pytest

def test_bulk_import_sql_exists():
    sql_file = '/home/user/bulk_import.sql'
    assert os.path.isfile(sql_file), f"Expected output file {sql_file} does not exist."

def test_bulk_import_sql_content():
    sql_file = '/home/user/bulk_import.sql'
    assert os.path.isfile(sql_file), f"Expected output file {sql_file} does not exist."

    with open(sql_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected exactly 4 non-empty lines in {sql_file}, but found {len(lines)}."

    expected_lines = {
        "INSERT INTO loc_data (string_id, locale, word_count, translated_text) VALUES ('ERR_01', 'fr', 3, 'Fichier non trouvé');",
        "INSERT INTO loc_data (string_id, locale, word_count, translated_text) VALUES ('BTN_OK', 'fr', 1, 'D''accord');",
        "INSERT INTO loc_data (string_id, locale, word_count, translated_text) VALUES ('MSG_GREET', 'es', 6, 'Bienvenido al sistema');",
        "INSERT INTO loc_data (string_id, locale, word_count, translated_text) VALUES ('MSG_BYE', 'it', 1, 'Arrivederci');"
    }

    actual_lines = set(lines)

    missing_lines = expected_lines - actual_lines
    extra_lines = actual_lines - expected_lines

    error_msg = []
    if missing_lines:
        error_msg.append(f"Missing expected lines:\n" + "\n".join(missing_lines))
    if extra_lines:
        error_msg.append(f"Unexpected extra lines:\n" + "\n".join(extra_lines))

    assert not missing_lines and not extra_lines, "\n".join(error_msg)