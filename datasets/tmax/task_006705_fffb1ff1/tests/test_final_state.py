# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_identified():
    actual_file = "/home/user/bad_commit.txt"
    expected_file = "/tmp/expected_bad_commit.txt"

    assert os.path.isfile(actual_file), f"File {actual_file} does not exist. Did you save the bad commit hash?"
    assert os.path.isfile(expected_file), f"Truth file {expected_file} is missing."

    with open(actual_file, "r") as f:
        actual_hash = f.read().strip()

    with open(expected_file, "r") as f:
        expected_hash = f.read().strip()

    assert actual_hash == expected_hash, f"The commit hash in {actual_file} is incorrect. Expected {expected_hash}, got {actual_hash}."

def test_cargo_test_passes():
    repo_dir = "/home/user/chrono_shift"
    try:
        subprocess.check_output(
            ["cargo", "test"],
            cwd=repo_dir,
            text=True,
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"'cargo test' failed in {repo_dir}. The bug is not fixed or tests are failing.\nOutput:\n{e.output}")

def test_test_parser_unmodified():
    test_file = "/home/user/chrono_shift/tests/test_parser.rs"
    assert os.path.isfile(test_file), f"File {test_file} does not exist."

    expected_content = """use chrono_shift::parser::parse_timezone;

#[test]
fn test_valid_timezone() {
    assert_eq!(parse_timezone("2023-10-12T05:00:00-05:00"), Ok("-05:00"));
}

#[test]
fn test_corrupted_timezone() {
    // Too short
    assert_eq!(parse_timezone("2023-10-12"), Err("Invalid Timezone"));

    // Invalid character boundary at index 19
    let bad_str = "2023-10-12T05:00:0\\u{2800}Z"; 
    assert_eq!(parse_timezone(bad_str), Err("Invalid Timezone"));
}
"""
    with open(test_file, "r") as f:
        actual_content = f.read()

    # Normalize line endings and strip whitespace
    assert actual_content.strip() == expected_content.strip(), f"The tests file {test_file} was modified. You should only modify src/parser.rs."