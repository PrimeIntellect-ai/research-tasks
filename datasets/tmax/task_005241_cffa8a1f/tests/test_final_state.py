# test_final_state.py

import os
import subprocess
import pytest

def test_bad_commit_hash():
    expected_path = "/tmp/expected_bad_commit.txt"
    actual_path = "/home/user/bad_commit_hash.txt"

    assert os.path.isfile(actual_path), f"File {actual_path} does not exist."

    with open(expected_path, 'r') as f:
        expected_hash = f.read().strip()

    with open(actual_path, 'r') as f:
        actual_hash = f.read().strip()

    assert actual_hash == expected_hash, f"Expected bad commit hash {expected_hash}, but got {actual_hash}."

def test_fixed_parser_exists():
    fixed_parser_path = "/home/user/fixed_parser.rs"
    assert os.path.isfile(fixed_parser_path), f"Fixed parser file {fixed_parser_path} does not exist."

def test_fixed_parser_uses_threading():
    fixed_parser_path = "/home/user/fixed_parser.rs"
    with open(fixed_parser_path, 'r') as f:
        content = f.read()

    assert "thread::spawn" in content, "The fixed parser does not appear to use thread::spawn for concurrency."

def test_fixed_parser_compiles_and_runs(tmp_path):
    fixed_parser_path = "/home/user/fixed_parser.rs"
    repo_path = "/home/user/log_parser_repo"

    # Compile the fixed parser
    output_bin = tmp_path / "fixed_parser"
    compile_result = subprocess.run(
        ["rustc", fixed_parser_path, "-o", str(output_bin)],
        capture_output=True,
        text=True
    )
    assert compile_result.returncode == 0, f"Failed to compile {fixed_parser_path}:\n{compile_result.stderr}"

    # Run the compiled binary 50 times to ensure no race conditions
    for i in range(50):
        run_result = subprocess.run(
            [str(output_bin)],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        assert run_result.returncode == 0, f"Run {i+1}/50 failed due to a race condition or other error:\n{run_result.stderr}"

def test_test_log_unmodified():
    log_path = "/home/user/log_parser_repo/test.log"
    assert os.path.isfile(log_path), f"test.log missing at {log_path}."

    with open(log_path, 'r') as f:
        lines = f.readlines()
    assert len(lines) == 1006, f"Expected test.log to have 1006 lines, but found {len(lines)}. The file was modified."
    assert lines[0].strip() == "INFO: system started", "test.log content was modified."
    assert lines[-1].strip() == "INFO: line 1000", "test.log content was modified."