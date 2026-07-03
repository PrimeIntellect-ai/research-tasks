# test_final_state.py

import os
import pytest
import csv

def test_clean_data_exists_and_content():
    clean_data_path = "/home/user/clean_data.csv"

    assert os.path.isfile(clean_data_path), f"File {clean_data_path} does not exist. Did you run the Go script?"

    expected_rows = [
        ["id", "age", "age_group", "review_tokens"],
        ["123e4567-e89b-12d3-a456-426614174000", "25", "youth", "great|product|highly|recommend"],
        ["123e4567-e89b-12d3-a456-426614174003", "65", "senior", "works|well|very|sturdy"],
        ["123e4567-e89b-12d3-a456-426614174004", "45", "adult", "awful|terrible"],
        ["123e4567-e89b-12d3-a456-426614174006", "30", "adult", "lots|of|spaces"]
    ]

    actual_rows = []
    with open(clean_data_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            actual_rows.append(row)

    assert actual_rows == expected_rows, f"Content of {clean_data_path} does not match the expected final state."

def test_process_go_exists():
    script_path = "/home/user/process.go"
    assert os.path.isfile(script_path), f"Go script {script_path} does not exist."