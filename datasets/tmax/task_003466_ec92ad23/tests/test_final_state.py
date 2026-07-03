# test_final_state.py

import os
import json
import pytest

def test_compiled_locales_file_exists():
    """Verify that the output JSONL file has been created."""
    output_file = "/home/user/compiled_locales.jsonl"
    assert os.path.isfile(output_file), f"Output file is missing: {output_file}"

def test_compiled_locales_content():
    """Verify that the JSONL file contains the correctly parsed, converted, and sorted records."""
    output_file = "/home/user/compiled_locales.jsonl"

    # Expected data after parsing, timezone conversion, and sorting
    expected_data = [
        {"timestamp": "2023-11-01T12:30:00Z", "lang_code": "es-ES", "original_text": "Settings", "translated_text": "Ajustes"},
        {"timestamp": "2023-11-01T12:30:00Z", "lang_code": "fr-FR", "original_text": "Welcome", "translated_text": "Bienvenue"},
        {"timestamp": "2023-11-01T13:00:00Z", "lang_code": "de-DE", "original_text": "Multi\nLine\nTest", "translated_text": "Mehrzeiliger\nTest\nHier"},
        {"timestamp": "2023-11-01T13:15:00Z", "lang_code": "ja-JP", "original_text": "Warning:\nLow Battery", "translated_text": "警告:\nバッテリー低下"},
        {"timestamp": "2023-11-01T15:30:00Z", "lang_code": "hi-IN", "original_text": "Submit", "translated_text": "प्रस्तुत"},
        {"timestamp": "2023-11-01T16:45:00Z", "lang_code": "es-MX", "original_text": "Error occurred", "translated_text": "Ocurrió un error\nPor favor intente de nuevo"}
    ]

    actual_data = []
    with open(output_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                actual_data.append(record)
            except json.JSONDecodeError:
                pytest.fail(f"Line {line_num} in {output_file} is not valid JSON: {line}")

    assert len(actual_data) == len(expected_data), (
        f"Expected {len(expected_data)} records, but found {len(actual_data)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_data, expected_data)):
        assert actual == expected, (
            f"Record at index {i} does not match expected.\n"
            f"Actual:   {actual}\n"
            f"Expected: {expected}"
        )