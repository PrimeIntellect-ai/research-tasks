# test_final_state.py

import os
import pytest

def test_translations_wide_csv():
    file_path = "/home/user/translations_wide.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you save the wide format data?"

    expected_content = (
        "key,en,fr,es\n"
        "BTN_CANCEL,Cancel,Annuler!,\n"
        "BTN_OK,Okay,D'accord,Aceptar\n"
        "ERR_404,Not Found,,No Encontrado\n"
        "TITLE_MAIN,Main Menu,Menu Principal,Menu Principal\n"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Strip trailing newlines for a more robust comparison
    assert content.strip() == expected_content.strip(), f"Content of {file_path} does not match the expected reshaped data."

def test_sample_qa_csv():
    file_path = "/home/user/sample_qa.csv"
    assert os.path.isfile(file_path), f"File {file_path} is missing. Did you save the QA sample data?"

    expected_content = (
        "key,en,fr,es\n"
        "BTN_OK,Okay,D'accord,Aceptar\n"
        "TITLE_MAIN,Main Menu,Menu Principal,Menu Principal\n"
    )

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Strip trailing newlines for a more robust comparison
    assert content.strip() == expected_content.strip(), f"Content of {file_path} does not match the expected QA sample data."