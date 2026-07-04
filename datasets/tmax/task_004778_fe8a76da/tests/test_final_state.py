# test_final_state.py

import os
import subprocess
import pytest

def test_bug_report_content():
    report_path = "/home/user/bug_report.txt"
    assert os.path.isfile(report_path), f"The bug report file {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_content = "Line content: 2023-10-12T14:32:01Z 10.0.0.42"
    assert content == expected_content, f"The bug report content is incorrect. Expected: '{expected_content}', but got: '{content}'"

def test_cargo_run_success():
    project_dir = "/home/user/log-parser"
    log_file = "/home/user/logs/server.log"

    result = subprocess.run(
        ["cargo", "run", "--", log_file],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"`cargo run` failed with exit code {result.returncode}.\nStderr: {result.stderr}"
    assert "Successfully parsed" in result.stdout, "The output does not indicate successful parsing of lines."

def test_cargo_test_success():
    project_dir = "/home/user/log-parser"

    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"`cargo test` failed with exit code {result.returncode}.\nStderr: {result.stderr}"
    assert "test_malformed_line" in result.stdout, "The output of `cargo test` does not indicate that `test_malformed_line` was run."

def test_main_rs_contains_test():
    main_rs_path = "/home/user/log-parser/src/main.rs"
    assert os.path.isfile(main_rs_path), f"The source file {main_rs_path} is missing."

    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "fn test_malformed_line" in content, "The function `test_malformed_line` is missing from main.rs."