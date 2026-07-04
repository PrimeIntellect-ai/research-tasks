# test_final_state.py

import os
import json
import unicodedata
import pytest

OUTPUT_FILE = "/home/user/loc_pipeline/normalized_translations.jsonl"

def test_output_file_exists():
    assert os.path.isfile(OUTPUT_FILE), f"Expected output file {OUTPUT_FILE} does not exist."

def test_output_content():
    assert os.path.isfile(OUTPUT_FILE), "Output file missing."

    records = []
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                records.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} is not valid JSON: {line}")

    # Check structure
    for rec in records:
        assert set(rec.keys()) == {"key", "locale", "translation"}, f"Record has incorrect keys: {rec}"

        # Check NFC normalization
        for v in rec.values():
            if isinstance(v, str):
                assert v == unicodedata.normalize('NFC', v), f"String '{v}' is not NFC normalized."

    # Group by key and locale
    data_map = {}
    for rec in records:
        k = rec["key"]
        loc = rec["locale"]
        if k not in data_map:
            data_map[k] = {}
        data_map[k][loc] = rec["translation"]

    # 1. No records with key == "msg_welcome"
    assert "msg_welcome" not in data_map, "Key 'msg_welcome' should have been dropped because 'en' is empty."

    # 2. btn_cancel for locale fr has translation "Annuler (updated)"
    assert "btn_cancel" in data_map, "Missing 'btn_cancel' key."
    assert data_map["btn_cancel"].get("fr") == "Annuler (updated)", "FR translation for 'btn_cancel' did not update correctly."

    # 3. lbl_user has records for en, es, fr, ar
    assert "lbl_user" in data_map, "Missing 'lbl_user' key."
    lbl_user_locales = set(data_map["lbl_user"].keys())
    assert lbl_user_locales == {"en", "es", "fr", "ar"}, f"Expected locales {{'en', 'es', 'fr', 'ar'}} for 'lbl_user', got {lbl_user_locales}"

    # 4. Full expected output verification
    expected_data = {
        "btn_submit": {
            "en": "Submit",
            "es": "Enviar",
            "ar": "إرسال"
        },
        "btn_cancel": {
            "en": "Cancel",
            "es": "Cancelar",
            "fr": "Annuler (updated)",
            "ja": "キャンセル"
        },
        "lbl_user": {
            "en": "User",
            "es": "Usuario",
            "fr": "Utilisateur",
            "ar": "مستخدم"
        },
        "emoji_test": {
            "en": "Hello 😊",
            "fr": "Bonjour",
            "ja": "こんにちは 😊"
        }
    }

    # Normalize expected data to NFC just in case
    for k in expected_data:
        for loc in expected_data[k]:
            expected_data[k][loc] = unicodedata.normalize('NFC', expected_data[k][loc])

    assert data_map == expected_data, "The final merged and reshaped data does not match the expected state."