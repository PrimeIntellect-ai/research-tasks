# test_final_state.py

import os
import pytest

def test_results_csv_exists():
    assert os.path.isfile("/home/user/results.csv"), "/home/user/results.csv does not exist. Did you compile and run your program to generate the output?"

def test_results_csv_content():
    expected_lines = [
        "LogID,UserID,Name,Region,MessageLength,MaskedMessage",
        "1,101,Alice,Europe,51,Hello [USER:101], please email [REDACTED] for help.",
        "2,103,Chlöe,Europe,46,¡Hola! [USER:103], contact us at [REDACTED].",
        "3,104,Daisuke,Asia,43,[USER:104] says こんにちは, my email is [REDACTED]!",
        "4,999,Unknown,Unknown,46,System message for [USER:999]: ping [REDACTED]"
    ]

    try:
        with open("/home/user/results.csv", "r", encoding="utf-8") as f:
            content = f.read().strip().splitlines()
    except UnicodeDecodeError:
        pytest.fail("/home/user/results.csv is not valid UTF-8. Did you handle Unicode correctly?")

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in results.csv, but found {len(content)}. Ensure you process all lines and include the header."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"