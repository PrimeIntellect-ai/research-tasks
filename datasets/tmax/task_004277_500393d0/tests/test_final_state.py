# test_final_state.py

import os
import csv
import xml.etree.ElementTree as ET
import pytest

def test_copied_csv_exists():
    path = "/home/user/workspace/translations.csv"
    assert os.path.exists(path), f"Copied CSV missing at {path}. Did you copy it from the remote directory?"

def test_long_csv():
    path = "/home/user/workspace/translations_long.csv"
    assert os.path.exists(path), f"Long CSV missing at {path}"

    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['string_id', 'locale', 'value'], f"CSV columns incorrect. Expected ['string_id', 'locale', 'value'], got {header}"

        rows = list(reader)
        assert len(rows) == 12, f"CSV should have exactly 12 data rows, found {len(rows)}"

        expected_rows = [
            ['greeting', 'en', 'Hello'],
            ['greeting', 'es', 'Hola'],
            ['greeting', 'fr', 'Bonjour'],
            ['farewell', 'en', 'Goodbye'],
            ['farewell', 'es', 'Adiós'],
            ['farewell', 'fr', 'Au revoir'],
            ['login', 'en', 'Log In'],
            ['login', 'es', 'Iniciar sesión'],
            ['login', 'fr', 'Connexion'],
            ['error_404', 'en', 'Not Found'],
            ['error_404', 'es', 'No encontrado'],
            ['error_404', 'fr', 'Introuvable']
        ]

        for er in expected_rows:
            assert er in rows, f"Expected row {er} not found in {path}"

def test_xml_outputs():
    expected_data = {
        'en': {
            'greeting': 'Hello',
            'farewell': 'Goodbye',
            'login': 'Log In',
            'error_404': 'Not Found'
        },
        'es': {
            'greeting': 'Hola',
            'farewell': 'Adiós',
            'login': 'Iniciar sesión',
            'error_404': 'No encontrado'
        },
        'fr': {
            'greeting': 'Bonjour',
            'farewell': 'Au revoir',
            'login': 'Connexion',
            'error_404': 'Introuvable'
        }
    }

    for loc, strings_dict in expected_data.items():
        xml_path = f"/home/user/workspace/output/values-{loc}/strings.xml"
        assert os.path.exists(xml_path), f"Missing XML output for locale '{loc}' at {xml_path}"

        try:
            tree = ET.parse(xml_path)
        except ET.ParseError as e:
            pytest.fail(f"Failed to parse XML at {xml_path}: {e}")

        root = tree.getroot()
        assert root.tag == 'resources', f"Root element should be 'resources' in {xml_path}, got '{root.tag}'"

        strings = root.findall('string')
        assert len(strings) == 4, f"Should be exactly 4 'string' elements in {xml_path}, found {len(strings)}"

        actual_strings = {el.get('name'): el.text for el in strings}
        for expected_name, expected_value in strings_dict.items():
            assert expected_name in actual_strings, f"Missing string name='{expected_name}' in {xml_path}"
            assert actual_strings[expected_name] == expected_value, f"Value mismatch for '{expected_name}' in {xml_path}. Expected '{expected_value}', got '{actual_strings[expected_name]}'"