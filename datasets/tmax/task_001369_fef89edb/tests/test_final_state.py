# test_final_state.py

import os
import csv
import unicodedata
import pytest

def test_cleaned_reviews_exists():
    assert os.path.isfile("/home/user/data/cleaned_reviews.csv"), "The output file /home/user/data/cleaned_reviews.csv is missing."

def test_cleaned_reviews_content():
    output_path = "/home/user/data/cleaned_reviews.csv"

    # Read the generated CSV
    rows = []
    with open(output_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
            assert header == ["id", "month", "review"], f"Header is incorrect. Expected ['id', 'month', 'review'], got {header}"
            for row in reader:
                rows.append(row)
        except StopIteration:
            pytest.fail("The CSV file is empty (missing header and data).")
        except UnicodeDecodeError as e:
            pytest.fail(f"The CSV file contains invalid UTF-8 bytes: {e}")

    # Expected data
    # Note: p1,2023_01 should be 'café' in NFC
    # p2,2023_01 had \xff\xfe which are 2 invalid bytes, so 2 replacement characters \uFFFD
    expected_rows = [
        ["p1", "2023_01", "caf\u00e9"],
        ["p1", "2023_03", "good"],
        ["p2", "2023_01", "\ufffd\ufffdhello"],
        ["p2", "2023_02", "Great"],
        ["p3", "2023_02", "ありがとう"],
        ["p3", "2023_03", "ممتاز"],
    ]

    assert len(rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_rows)):
        assert actual == expected, f"Row {i+1} is incorrect.\nExpected: {expected}\nActual:   {actual}"

def test_unicode_normalization():
    output_path = "/home/user/data/cleaned_reviews.csv"

    with open(output_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row_num, row in enumerate(reader, start=2):
            review = row.get("review", "")
            # Verify that the string is in NFC
            assert unicodedata.is_normalized("NFC", review), f"Row {row_num}: The review text '{review}' is not in Unicode Normalization Form C (NFC)."