# test_final_state.py

import os
import pytest

def test_makefile_exists():
    makefile_path = "/home/user/Makefile"
    assert os.path.isfile(makefile_path), f"{makefile_path} does not exist. A Makefile is required."

def test_cleaned_txt_content():
    cleaned_path = "/home/user/cleaned.txt"
    assert os.path.isfile(cleaned_path), f"{cleaned_path} does not exist. Make sure Stage 1 creates this file."

    expected_lines = [
        "hello world",
        "save file",
        "delete items",
        "user profiles",
        "save game"
    ]

    with open(cleaned_path, "r") as f:
        actual_lines = [line.strip() for line in f.read().strip().splitlines()]

    assert actual_lines == expected_lines, (
        f"Content of {cleaned_path} does not match expected output.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {actual_lines}"
    )

def test_localization_report_csv_content():
    csv_path = "/home/user/localization_report.csv"
    assert os.path.isfile(csv_path), f"{csv_path} does not exist. Make sure the Go program generates this file."

    expected_content = (
        "CleanedSource,BestMatchTarget,Distance,RollingAvg\n"
        "hello world,hola mundo,0,0.00\n"
        "save file,guardar archivo,0,0.00\n"
        "delete items,eliminar elemento,1,0.33\n"
        "user profiles,perfil de usuario,1,0.67\n"
        "save game,guardar archivo,4,2.00"
    )

    with open(csv_path, "r") as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"Content of {csv_path} does not match expected output.\n"
        f"Expected:\n{expected_content}\n"
        f"Got:\n{actual_content}"
    )