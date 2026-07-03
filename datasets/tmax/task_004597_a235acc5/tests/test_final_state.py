# test_final_state.py

import os
import pytest

def test_locales_directory_exists():
    locales_dir = "/home/user/locales"
    assert os.path.exists(locales_dir), f"Directory {locales_dir} does not exist."
    assert os.path.isdir(locales_dir), f"Path {locales_dir} is not a directory."

def test_en_locale_content():
    en_path = "/home/user/locales/en.h"
    assert os.path.exists(en_path), f"File {en_path} does not exist."

    with open(en_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_lines = [
        "#pragma once",
        "#include <string>",
        "namespace i18n_en {",
        'const std::string btn_cancel = "Cancel";',
        'const std::string btn_submit = "Submit Updated";',
        "}"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {en_path}"

    # Check order of keys
    idx_cancel = content.find("btn_cancel")
    idx_submit = content.find("btn_submit")
    assert idx_cancel < idx_submit, "Keys in en.h are not sorted alphabetically."

def test_fr_locale_content():
    fr_path = "/home/user/locales/fr.h"
    assert os.path.exists(fr_path), f"File {fr_path} does not exist."

    with open(fr_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_lines = [
        "#pragma once",
        "#include <string>",
        "namespace i18n_fr {",
        'const std::string btn_cancel = "Annuler";',
        'const std::string btn_submit = "Soumettre";',
        "}"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {fr_path}"

    # Check order of keys
    idx_cancel = content.find("btn_cancel")
    idx_submit = content.find("btn_submit")
    assert idx_cancel < idx_submit, "Keys in fr.h are not sorted alphabetically."

def test_es_locale_content():
    es_path = "/home/user/locales/es.h"
    assert os.path.exists(es_path), f"File {es_path} does not exist."

    with open(es_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_lines = [
        "#pragma once",
        "#include <string>",
        "namespace i18n_es {",
        'const std::string success = "Éxito";',
        "}"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {es_path}"

def test_no_invalid_locales():
    locales_dir = "/home/user/locales"
    if os.path.exists(locales_dir):
        files = os.listdir(locales_dir)
        valid_files = {"en.h", "fr.h", "es.h"}
        for f in files:
            assert f in valid_files, f"Unexpected file {f} found in {locales_dir}. Invalid entries should be skipped."