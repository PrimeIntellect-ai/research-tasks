# test_final_state.py

import os
import json
import configparser
import ast
import pytest

BASE_DIR = "/home/user/locales"
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
FINAL_JSON_PATH = os.path.join(OUTPUT_DIR, "final.json")
SCRIPT_PATH = "/home/user/process_locales.py"

EXPECTED_DATA = {
    "de": {
        "btn_cancel": "Abbrechen_new",
        "btn_submit": "Einreichen",
        "lbl_error": "Fehler",
        "msg_goodbye": "Auf Wiedersehen",
        "msg_welcome": "Willkommen"
    },
    "es": {
        "btn_cancel": "Cancelar_new",
        "btn_submit": "Enviar",
        "lbl_error": "Error",
        "msg_goodbye": "Adiós",
        "msg_welcome": "Bienvenido"
    },
    "fr": {
        "btn_cancel": "Annuler_new",
        "btn_submit": "Soumettre",
        "lbl_error": "Erreur",
        "msg_goodbye": "Au revoir",
        "msg_welcome": "Bienvenue"
    }
}

def test_script_exists_and_uses_parallelism():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=SCRIPT_PATH)

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)

    has_parallel = "multiprocessing" in imports or "concurrent.futures" in imports
    assert has_parallel, "Script does not import 'multiprocessing' or 'concurrent.futures'."

def test_final_json_content():
    assert os.path.isfile(FINAL_JSON_PATH), f"File {FINAL_JSON_PATH} does not exist."

    with open(FINAL_JSON_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{FINAL_JSON_PATH} is not a valid JSON file.")

    for locale, expected_translations in EXPECTED_DATA.items():
        assert locale in data, f"Locale '{locale}' missing from {FINAL_JSON_PATH}."
        for key, value in expected_translations.items():
            assert data[locale].get(key) == value, f"Translation mismatch in JSON for locale '{locale}', key '{key}'. Expected '{value}', got '{data[locale].get(key)}'."

@pytest.mark.parametrize("locale", ["es", "fr", "de"])
def test_ini_files_content(locale):
    ini_path = os.path.join(OUTPUT_DIR, f"final_{locale}.ini")
    assert os.path.isfile(ini_path), f"INI file {ini_path} does not exist."

    config = configparser.ConfigParser()
    # To preserve case of keys
    config.optionxform = str

    try:
        config.read(ini_path, encoding="utf-8")
    except configparser.Error as e:
        pytest.fail(f"Failed to parse {ini_path} as INI file: {e}")

    assert "translations" in config.sections(), f"Section [translations] missing in {ini_path}."

    actual_translations = dict(config["translations"])
    expected_translations = EXPECTED_DATA[locale]

    for key, expected_value in expected_translations.items():
        assert key in actual_translations, f"Key '{key}' missing in {ini_path}."
        assert actual_translations[key] == expected_value, f"Value for '{key}' in {ini_path} is incorrect. Expected '{expected_value}', got '{actual_translations[key]}'."

    assert len(actual_translations) == len(expected_translations), f"Extra keys found in {ini_path}."

def test_no_en_ini_file():
    en_ini_path = os.path.join(OUTPUT_DIR, "final_en.ini")
    assert not os.path.exists(en_ini_path), f"English INI file {en_ini_path} should not be generated."