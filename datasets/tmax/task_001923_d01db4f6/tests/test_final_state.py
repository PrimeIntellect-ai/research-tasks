# test_final_state.py

import os
import pytest

def test_c_source_exists():
    path = "/home/user/fuzzy_updater.c"
    assert os.path.exists(path), f"Source file {path} is missing."

def test_executable_exists():
    path = "/home/user/fuzzy_updater"
    assert os.path.exists(path), f"Executable file {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_updated_translations_output():
    path = "/home/user/updated_translations.tsv"
    assert os.path.exists(path), f"Output file {path} is missing."

    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "ERR_FILE_NOT_FOUND\tFile not found\tEl archivo no se encuentra\t3",
        "MSG_WELCOME\tWelcome to the system\tBienvenido a nuestro sistema\t3",
        "BTN_SUBMIT\tSubmit form\tEnviar el formulario\t4"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in output, got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"