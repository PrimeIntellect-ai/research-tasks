# test_final_state.py
import os
import csv
import pytest

def test_csv_exists_and_correct():
    csv_path = "/home/user/cross_country_collaborations.csv"
    assert os.path.isfile(csv_path), f"File {csv_path} does not exist. The script might not have been executed or saved it to the wrong path."

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "The generated CSV file is empty."

    headers = rows[0]
    expected_headers = ["author1_name", "author2_name", "author1_country", "author2_country", "paper_count"]
    assert headers == expected_headers, f"CSV headers are incorrect. Expected {expected_headers}, got {headers}."

    data_rows = rows[1:]
    expected_rows = [
        ["Alice Adams", "Bob Brown", "USA", "UK", "2"],
        ["Alice Adams", "David Davis", "USA", "Switzerland", "1"],
        ["Bob Brown", "Charlie Clark", "UK", "USA", "1"],
        ["Bob Brown", "David Davis", "UK", "Switzerland", "1"],
        ["Bob Brown", "Frank Ford", "UK", "USA", "1"],
        ["David Davis", "Eve Evans", "Switzerland", "UK", "1"]
    ]

    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, got {len(data_rows)}. Ensure you are filtering cross-country collaborations correctly."

    for i, (actual, expected) in enumerate(zip(data_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}. Check your sorting, alphabetical ordering of author pairs, and paper counts."