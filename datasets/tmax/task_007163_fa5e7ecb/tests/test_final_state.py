# test_final_state.py

import os
import subprocess
import pytest

MINIMAL_CRASH_BIN = "/home/user/data_parser/minimal_crash.bin"
FIXED_PARSER_C = "/home/user/data_parser/fixed_parser.c"
FIXED_PARSER_BIN = "/home/user/data_parser/fixed_parser"
TELEMETRY_BIN = "/home/user/data_parser/telemetry.bin"

def test_minimal_crash_bin():
    assert os.path.exists(MINIMAL_CRASH_BIN), f"{MINIMAL_CRASH_BIN} does not exist."
    with open(MINIMAL_CRASH_BIN, "rb") as f:
        content = f.read()

    expected_content = b"\xAA\xFF\xFF\xFF\xFF"
    assert content == expected_content, (
        f"minimal_crash.bin content is incorrect. "
        f"Expected {expected_content}, got {content}."
    )

def test_fixed_parser_exists():
    assert os.path.exists(FIXED_PARSER_C), f"{FIXED_PARSER_C} does not exist."
    assert os.path.exists(FIXED_PARSER_BIN), f"{FIXED_PARSER_BIN} does not exist."
    assert os.access(FIXED_PARSER_BIN, os.X_OK), f"{FIXED_PARSER_BIN} is not executable."

def test_fixed_parser_minimal_crash():
    assert os.path.exists(FIXED_PARSER_BIN), "fixed_parser executable missing."
    assert os.path.exists(MINIMAL_CRASH_BIN), "minimal_crash.bin missing."

    result = subprocess.run(
        [FIXED_PARSER_BIN, MINIMAL_CRASH_BIN],
        capture_output=True,
        text=True
    )

    assert result.returncode == 2, f"Expected exit code 2, got {result.returncode}."
    assert result.stderr.strip() == "ERROR: CORRUPTED INPUT", (
        f"Expected stderr 'ERROR: CORRUPTED INPUT', got '{result.stderr}'."
    )

def test_fixed_parser_telemetry_bin():
    assert os.path.exists(FIXED_PARSER_BIN), "fixed_parser executable missing."
    assert os.path.exists(TELEMETRY_BIN), "telemetry.bin missing."

    result = subprocess.run(
        [FIXED_PARSER_BIN, TELEMETRY_BIN],
        capture_output=True,
        text=True
    )

    assert result.returncode == 2, f"Expected exit code 2, got {result.returncode}."
    assert result.stderr.strip() == "ERROR: CORRUPTED INPUT", (
        f"Expected stderr 'ERROR: CORRUPTED INPUT', got '{result.stderr}'."
    )