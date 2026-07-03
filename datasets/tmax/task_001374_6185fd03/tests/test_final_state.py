# test_final_state.py

import os
import csv
import math
import pytest

CLEANED_CSV_PATH = '/home/user/cleaned_reviews.csv'
CORRELATION_TXT_PATH = '/home/user/correlation.txt'

def test_cleaned_csv_exists():
    assert os.path.isfile(CLEANED_CSV_PATH), f"{CLEANED_CSV_PATH} does not exist. Did you save the cleaned dataset?"

def test_cleaned_csv_content():
    expected_rows = [
        ['1', 'Great product, loved it.', '5', '10.5', '4'],
        ['2', 'Terrible. Do not buy.', '1', '15.0', '4'],
        ['6', 'Average.', '3', '10.0', '1'],
        ['7', 'I am absolutely amazed by the quality of this item.', '5', '25.0', '10'],
        ['8', 'Broke after one use', '1', '8.0', '4'],
        ['9', 'It is fine', '3', '11.5', '3'],
        ['10', 'Not what I expected', '2', '9.99', '4']
    ]

    with open(CLEANED_CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{CLEANED_CSV_PATH} is empty."

    header = rows[0]
    expected_header = ['ReviewID', 'Text', 'Rating', 'Price', 'TokenCount']
    assert header == expected_header, f"Header in {CLEANED_CSV_PATH} is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but found {len(data_rows)}."

    for i, expected in enumerate(expected_rows):
        assert data_rows[i] == expected, f"Row {i+1} mismatch. Expected {expected}, got {data_rows[i]}."

def test_correlation_txt_exists():
    assert os.path.isfile(CORRELATION_TXT_PATH), f"{CORRELATION_TXT_PATH} does not exist. Did you save the correlation coefficient?"

def test_correlation_value():
    with open(CORRELATION_TXT_PATH, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected_val = "0.3845"
    assert content == expected_val, f"Incorrect correlation value in {CORRELATION_TXT_PATH}. Expected '{expected_val}', got '{content}'."