# test_final_state.py

import os
import subprocess
import pytest

API_PARSER_DIR = "/home/user/api_parser"
WORKSPACE_DIR = "/home/user/workspace"

def test_directories_created():
    """Verify that the new project directories have been created."""
    for d in ["src", "include", "tests"]:
        dir_path = os.path.join(API_PARSER_DIR, d)
        assert os.path.isdir(dir_path), f"Directory {dir_path} was not created."

def test_files_moved():
    """Verify that the files were correctly moved to their new locations."""
    expected_files = {
        "src/http_parser.c": "http_parser.c",
        "include/http_parser.h": "http_parser.h",
        "tests/test_http_parser.c": "test_http_parser.c"
    }

    for new_rel_path, old_name in expected_files.items():
        new_path = os.path.join(API_PARSER_DIR, new_rel_path)
        old_path = os.path.join(WORKSPACE_DIR, old_name)

        assert os.path.isfile(new_path), f"File {new_path} is missing. It should have been moved here."
        assert not os.path.exists(old_path), f"File {old_path} still exists. It should have been moved, not copied."

def test_test_summary_content():
    """Verify that test_summary.txt was generated and contains the correct output."""
    summary_path = os.path.join(API_PARSER_DIR, "test_summary.txt")
    assert os.path.isfile(summary_path), f"File {summary_path} is missing. Did you run the 'test' target?"

    with open(summary_path, "r") as f:
        content = f.read().strip()

    assert content == "ALL TESTS PASSED", f"Expected test_summary.txt to contain 'ALL TESTS PASSED', but got '{content}'."

def test_makefile_exists_and_works():
    """Verify the Makefile exists and implements the requested targets."""
    makefile_path = os.path.join(API_PARSER_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}."

    # Test 'clean' target
    clean_proc = subprocess.run(["make", "clean"], cwd=API_PARSER_DIR, capture_output=True)
    assert clean_proc.returncode == 0, "Failed to run 'make clean'."

    # Verify outputs are removed
    assert not os.path.exists(os.path.join(API_PARSER_DIR, "libparser.a")), "'make clean' did not remove libparser.a"
    assert not os.path.exists(os.path.join(API_PARSER_DIR, "test_runner")), "'make clean' did not remove test_runner"
    assert not os.path.exists(os.path.join(API_PARSER_DIR, "test_summary.txt")), "'make clean' did not remove test_summary.txt"

    # Test 'test' target
    test_proc = subprocess.run(["make", "test"], cwd=API_PARSER_DIR, capture_output=True)
    assert test_proc.returncode == 0, "Failed to run 'make test'."

    # Verify outputs are recreated
    summary_path = os.path.join(API_PARSER_DIR, "test_summary.txt")
    assert os.path.isfile(summary_path), "'make test' did not generate test_summary.txt"

    with open(summary_path, "r") as f:
        content = f.read().strip()
    assert content == "ALL TESTS PASSED", f"After running 'make test', expected 'ALL TESTS PASSED' in summary, got '{content}'."