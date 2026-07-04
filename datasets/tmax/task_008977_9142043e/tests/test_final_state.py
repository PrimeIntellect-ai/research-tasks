# test_final_state.py

import os
import re
import pytest

def test_merged_tsv_content():
    """Check if merged.tsv exists and matches the expected content."""
    filepath = "/home/user/translations/merged.tsv"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_lines = [
        "key\ten\tfr\tja\tes",
        "greeting\tHello\tBonjour\tこんにちは\tHola",
        "farewell\tGoodbye\tAu revoir\t\tAdiós",
        "apple\tApple\t\tりんご\tManzana"
    ]
    expected_content = "\n".join(expected_lines)

    # Compare line by line to give better error messages
    actual_lines = content.splitlines()
    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in merged.tsv, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in merged.tsv does not match.\nExpected: {repr(expected)}\nActual: {repr(actual)}"

def test_stats_txt_content():
    """Check if stats.txt exists and matches the expected content."""
    filepath = "/home/user/translations/stats.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_lines = [
        "en: 100%, 17",
        "fr: 66%, 16",
        "ja: 66%, 8",
        "es: 100%, 16"
    ]

    actual_lines = content.splitlines()
    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in stats.txt, found {len(actual_lines)}."

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in stats.txt does not match.\nExpected: {repr(expected)}\nActual: {repr(actual)}"

def test_run_pipeline_sh():
    """Check if run_pipeline.sh exists and is executable."""
    filepath = "/home/user/run_pipeline.sh"
    assert os.path.isfile(filepath), f"Script {filepath} is missing."
    assert os.access(filepath, os.X_OK), f"Script {filepath} is not executable."

def test_cron_schedule_txt():
    """Check if cron_schedule.txt contains the correct cron expression."""
    filepath = "/home/user/cron_schedule.txt"
    assert os.path.isfile(filepath), f"File {filepath} is missing."

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read().strip()

    # Pattern to match: 30 2 * * 0 /home/user/run_pipeline.sh (or 7, or sun/sunday)
    pattern = r"^\s*30\s+2\s+\*\s+\*\s+(0|7|sun|sunday)\s+/home/user/run_pipeline\.sh\s*$"

    assert re.match(pattern, content, re.IGNORECASE), f"Content of {filepath} does not match the expected cron expression for 2:30 AM on Sunday running /home/user/run_pipeline.sh. Found: {content}"