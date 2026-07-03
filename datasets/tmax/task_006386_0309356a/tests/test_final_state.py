# test_final_state.py

import os
import json
import pytest

def test_loc_clean_json_exists():
    """Check if the loc_clean.json file was created."""
    output_file = "/home/user/loc_clean.json"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. The Rust program may not have run or failed."

def test_loc_clean_json_content():
    """Check if the loc_clean.json file contains the correctly parsed and decoded data."""
    output_file = "/home/user/loc_clean.json"

    with open(output_file, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse {output_file} as JSON: {e}")

    expected_data = {
        "de-DE": {
            "FAREWELL": "Auf Wiedersehen",
            "GREETING": "Hallo Welt"
        },
        "es-ES": {
            "FAREWELL": "Adiós",
            "GREETING": "Hola Mundo"
        },
        "fr-FR": {
            "FAREWELL": "Au revoir",
            "GREETING": "Bonjour le monde"
        },
        "jp-JP": {
            "GREETING": "こんにちは"
        }
    }

    assert data == expected_data, "The contents of loc_clean.json do not match the expected grouped and decoded translations."

def test_loc_clean_json_formatting():
    """Check if the output is pretty-printed with 2 spaces indentation and sorted keys."""
    output_file = "/home/user/loc_clean.json"

    with open(output_file, "r", encoding="utf-8") as f:
        raw_content = f.read()

    # Check for 2-space indentation by looking at the first nested key
    assert '  "de-DE": {' in raw_content or '  "es-ES": {' in raw_content, "The JSON does not appear to be pretty-printed with 2 spaces of indentation."

    # Verify that the keys are alphabetically sorted in the text
    # The expected output string with 2 spaces
    expected_data = {
        "de-DE": {
            "FAREWELL": "Auf Wiedersehen",
            "GREETING": "Hallo Welt"
        },
        "es-ES": {
            "FAREWELL": "Adiós",
            "GREETING": "Hola Mundo"
        },
        "fr-FR": {
            "FAREWELL": "Au revoir",
            "GREETING": "Bonjour le monde"
        },
        "jp-JP": {
            "GREETING": "こんにちは"
        }
    }

    expected_raw = json.dumps(expected_data, indent=2, ensure_ascii=False)

    # We allow minor differences like trailing newlines
    assert raw_content.strip() == expected_raw.strip(), "The JSON formatting or sorting does not exactly match the expected pretty-printed output."