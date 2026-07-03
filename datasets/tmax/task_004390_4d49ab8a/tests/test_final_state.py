# test_final_state.py

import os
import csv
import json
import pytest
from datetime import datetime

def parse_rfc3339(timestamp_str):
    """Attempt to parse an RFC3339 string to a datetime object."""
    if timestamp_str.endswith('Z'):
        timestamp_str = timestamp_str[:-1] + '+00:00'
    try:
        return datetime.fromisoformat(timestamp_str)
    except ValueError:
        return None

def compute_expected_states(raw_csv_path):
    expected_invalid = []
    valid_dict = {}  # (lang_code, translation_key) -> dict of row data

    valid_langs = {'en-us', 'fr-fr', 'es-es', 'de-de', 'ja-jp'}

    with open(raw_csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return [], []

        for row in reader:
            if len(row) != 5:
                expected_invalid.append(row)
                continue

            timestamp_str, translator_id_str, lang_code_raw, translation_key, translated_text = row

            # Validation
            is_valid = True

            # 1. Timestamp
            dt = parse_rfc3339(timestamp_str)
            if dt is None:
                is_valid = False

            # 2. Lang code
            lang_code = lang_code_raw.lower()
            if lang_code not in valid_langs:
                is_valid = False

            # 3. Translator ID
            try:
                translator_id = int(translator_id_str)
            except ValueError:
                is_valid = False

            # 4. Translation key
            if not translation_key:
                is_valid = False

            # 5. Translated text
            if not translated_text:
                is_valid = False

            if not is_valid:
                expected_invalid.append(row)
            else:
                key = (lang_code, translation_key)
                current_entry = {
                    "timestamp": timestamp_str,
                    "translator_id": translator_id,
                    "lang_code": lang_code,
                    "translation_key": translation_key,
                    "translated_text": translated_text,
                    "_dt": dt
                }

                if key not in valid_dict:
                    valid_dict[key] = current_entry
                else:
                    existing_dt = valid_dict[key]["_dt"]
                    # If strictly greater, replace. If equal, keep first encountered (do nothing).
                    if dt > existing_dt:
                        valid_dict[key] = current_entry

    # Prepare expected JSONL
    expected_jsonl = []
    # Sort by lang_code, then translation_key
    for key in sorted(valid_dict.keys()):
        entry = valid_dict[key].copy()
        del entry["_dt"]
        expected_jsonl.append(entry)

    return expected_invalid, expected_jsonl

@pytest.fixture(scope="module")
def expected_data():
    raw_csv_path = '/home/user/raw_translations.csv'
    assert os.path.exists(raw_csv_path), f"Input file {raw_csv_path} is missing."
    return compute_expected_states(raw_csv_path)

def test_invalid_rows_csv(expected_data):
    """Test that invalid_rows.csv contains exactly the expected invalid rows."""
    expected_invalid, _ = expected_data
    invalid_csv_path = '/home/user/invalid_rows.csv'

    assert os.path.exists(invalid_csv_path), f"Output file {invalid_csv_path} does not exist."

    actual_invalid = []
    with open(invalid_csv_path, 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            actual_invalid.append(row)

    assert len(actual_invalid) == len(expected_invalid), (
        f"Expected {len(expected_invalid)} invalid rows, but found {len(actual_invalid)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_invalid, expected_invalid)):
        assert actual == expected, f"Row {i+1} in invalid_rows.csv mismatch. Expected: {expected}, Actual: {actual}"

def test_latest_translations_jsonl(expected_data):
    """Test that latest_translations.jsonl contains the correctly deduplicated and sorted valid rows."""
    _, expected_jsonl = expected_data
    jsonl_path = '/home/user/latest_translations.jsonl'

    assert os.path.exists(jsonl_path), f"Output file {jsonl_path} does not exist."

    actual_jsonl = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
                actual_jsonl.append(parsed)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {jsonl_path} is not valid JSON: {line}")

    assert len(actual_jsonl) == len(expected_jsonl), (
        f"Expected {len(expected_jsonl)} valid JSON lines, but found {len(actual_jsonl)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_jsonl, expected_jsonl)):
        assert actual == expected, (
            f"Line {i+1} in latest_translations.jsonl mismatch.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )