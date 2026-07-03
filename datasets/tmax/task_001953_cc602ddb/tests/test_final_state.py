# test_final_state.py

import os
import csv
import pytest

LONG_FORMAT_PATH = "/home/user/output/long_format.csv"
SAMPLE_PATH = "/home/user/output/sample.csv"
PIPELINE_LOG_PATH = "/home/user/pipeline.log"

EXPECTED_HEADER = ["UserID", "Region", "Day", "ProductID", "Sentiment", "ErrorCode"]

EXPECTED_LONG_ROWS = [
    ["U01", "NA", "Mon", "AppA", "positive", "none"],
    ["U01", "NA", "Tue", "AppB", "negative", "E100"],
    ["U01", "NA", "Wed", "AppA", "neutral", "none"],
    ["U02", "EU", "Mon", "AppC", "positive", "none"],
    ["U02", "EU", "Fri", "AppA", "negative", "E500"],
    ["U03", "NA", "Tue", "AppB", "negative", "E100"],
    ["U03", "NA", "Thu", "AppC", "positive", "none"],
    ["U04", "NA", "Wed", "AppA", "positive", "none"],
    ["U04", "NA", "Fri", "AppC", "positive", "none"],
    ["U05", "EU", "Mon", "AppA", "neutral", "none"],
    ["U05", "EU", "Tue", "AppB", "negative", "E200"],
    ["U05", "EU", "Wed", "AppB", "negative", "E201"],
    ["U06", "AS", "Thu", "AppA", "positive", "none"],
    ["U06", "AS", "Fri", "AppC", "neutral", "none"],
]

EXPECTED_SAMPLE_ROWS = [
    ["U01", "NA", "Mon", "AppA", "positive", "none"],
    ["U03", "NA", "Thu", "AppC", "positive", "none"],
    ["U01", "NA", "Tue", "AppB", "negative", "E100"],
    ["U03", "NA", "Tue", "AppB", "negative", "E100"],
    ["U01", "NA", "Wed", "AppA", "neutral", "none"],
    ["U02", "EU", "Mon", "AppC", "positive", "none"],
    ["U02", "EU", "Fri", "AppA", "negative", "E500"],
    ["U05", "EU", "Tue", "AppB", "negative", "E200"],
    ["U05", "EU", "Mon", "AppA", "neutral", "none"],
    ["U06", "AS", "Thu", "AppA", "positive", "none"],
    ["U06", "AS", "Fri", "AppC", "neutral", "none"],
]

def read_csv(path):
    with open(path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        rows = list(reader)
    return header, rows

def test_long_format_csv():
    assert os.path.isfile(LONG_FORMAT_PATH), f"File {LONG_FORMAT_PATH} does not exist."

    header, rows = read_csv(LONG_FORMAT_PATH)
    assert header == EXPECTED_HEADER, f"Header in {LONG_FORMAT_PATH} is incorrect. Expected {EXPECTED_HEADER}, got {header}."

    # Order doesn't matter for long_format.csv
    sorted_expected = sorted(EXPECTED_LONG_ROWS)
    sorted_actual = sorted(rows)

    assert len(sorted_actual) == len(sorted_expected), f"Expected {len(sorted_expected)} rows in {LONG_FORMAT_PATH}, but got {len(sorted_actual)}."
    assert sorted_actual == sorted_expected, f"Rows in {LONG_FORMAT_PATH} do not match expected data."

def test_sample_csv():
    assert os.path.isfile(SAMPLE_PATH), f"File {SAMPLE_PATH} does not exist."

    header, rows = read_csv(SAMPLE_PATH)
    assert header == EXPECTED_HEADER, f"Header in {SAMPLE_PATH} is incorrect. Expected {EXPECTED_HEADER}, got {header}."

    # Order of strata in sample.csv is not strictly enforced by the task, but the exact subset of rows is.
    sorted_expected = sorted(EXPECTED_SAMPLE_ROWS)
    sorted_actual = sorted(rows)

    assert len(sorted_actual) == len(sorted_expected), f"Expected {len(sorted_expected)} rows in {SAMPLE_PATH}, but got {len(sorted_actual)}."
    assert sorted_actual == sorted_expected, f"Rows in {SAMPLE_PATH} do not match the expected stratified sample."

def test_pipeline_log():
    assert os.path.isfile(PIPELINE_LOG_PATH), f"File {PIPELINE_LOG_PATH} does not exist."

    with open(PIPELINE_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_lines = [
        "[INFO] Processed 6 input rows.",
        "[INFO] Generated 14 long records.",
        "[INFO] Stratified sample size: 11."
    ]

    for line in expected_lines:
        assert line in content, f"Expected log line '{line}' not found in {PIPELINE_LOG_PATH}."