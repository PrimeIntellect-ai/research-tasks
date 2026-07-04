# test_final_state.py

import os
import csv
import hashlib
import pytest

OUTPUT_DIR = "/home/user/locales_processed"
CSV_PATH = os.path.join(OUTPUT_DIR, "unified_translations.csv")
PARQUET_PATH = os.path.join(OUTPUT_DIR, "unified_translations.parquet")

def test_output_directory_exists():
    assert os.path.isdir(OUTPUT_DIR), f"Expected output directory {OUTPUT_DIR} does not exist."

def test_parquet_file_exists():
    assert os.path.isfile(PARQUET_PATH), f"Expected Parquet file {PARQUET_PATH} does not exist."
    assert os.path.getsize(PARQUET_PATH) > 0, f"Parquet file {PARQUET_PATH} is empty."

def test_csv_file_exists_and_columns():
    assert os.path.isfile(CSV_PATH), f"Expected CSV file {CSV_PATH} does not exist."

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"CSV file {CSV_PATH} is empty.")

        expected_headers = ['hash_id', 'key', 'language', 'translation']
        assert headers == expected_headers, f"Expected columns {expected_headers}, got {headers}."

def test_csv_data_correctness_and_sorting():
    assert os.path.isfile(CSV_PATH), f"Expected CSV file {CSV_PATH} does not exist."

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 12, f"Expected exactly 12 translation rows, got {len(rows)}."

    # Check sorting: by key, then language
    keys_languages = [(row['key'], row['language']) for row in rows]
    sorted_keys_languages = sorted(keys_languages)
    assert keys_languages == sorted_keys_languages, "The dataset is not sorted alphabetically by 'key', then by 'language'."

    # Check hash_id correctness
    for row in rows:
        expected_hash = hashlib.sha256(f"{row['key']}_{row['language']}".encode('utf-8')).hexdigest()
        assert row['hash_id'] == expected_hash, f"Incorrect hash_id for {row['key']}_{row['language']}. Expected {expected_hash}, got {row['hash_id']}."

    # Convert to a dict for easy lookup
    translations = {f"{row['key']}_{row['language']}": row['translation'] for row in rows}

    # Verify specific overrides and values
    expected_values = {
        'greeting_en': 'Hello',        # App overrides Web ('Hi')
        'greeting_es': 'Hola',         # App overrides Web ('Hola Web')
        'greeting_fr': 'Bonjour',      # Web only
        'greeting_de': 'Hallo',        # Web only
        'farewell_en': 'Goodbye',      # App only
        'submit_en': 'Submit',         # App overrides Web ('Send')
        'submit_fr': 'Envoyer',        # Web only
        'submit_de': 'Einreichen',     # App overrides missing/null Web
        'login_en': 'Log In',          # Web only
        'login_es': 'Iniciar',         # Web only
        'login_fr': 'Connexion',       # Web only
        'login_de': 'Anmelden'         # Web only
    }

    for key_lang, expected_trans in expected_values.items():
        assert key_lang in translations, f"Missing expected translation entry for {key_lang}."
        actual_trans = translations[key_lang]
        assert actual_trans == expected_trans, f"Incorrect translation for {key_lang}. Expected '{expected_trans}', got '{actual_trans}'."