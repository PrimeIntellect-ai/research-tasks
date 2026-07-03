# test_final_state.py

import os
import pytest

def test_binaries_exist_and_executable():
    parser_path = "/home/user/bin/parser"
    verifier_path = "/home/user/bin/verifier"

    assert os.path.exists(parser_path), f"Binary {parser_path} does not exist."
    assert os.path.isfile(parser_path), f"{parser_path} is not a file."
    assert os.access(parser_path, os.X_OK), f"Binary {parser_path} is not executable."

    assert os.path.exists(verifier_path), f"Binary {verifier_path} does not exist."
    assert os.path.isfile(verifier_path), f"{verifier_path} is not a file."
    assert os.access(verifier_path, os.X_OK), f"Binary {verifier_path} is not executable."

def test_artifact_report_content():
    report_path = "/home/user/artifact_report.txt"
    assert os.path.exists(report_path), f"Report file {report_path} does not exist."
    assert os.path.isfile(report_path), f"{report_path} is not a file."

    with open(report_path, "r") as f:
        lines = f.read().splitlines()

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_path}, found {len(lines)}."

    expected_line1 = "METADATA: Build_v1.0.42_Release"
    expected_line2 = "CHECKSUM: 06FE for length 21"

    assert lines[0] == expected_line1, f"First line of report is incorrect. Expected '{expected_line1}', got '{lines[0]}'."
    assert lines[1] == expected_line2, f"Second line of report is incorrect. Expected '{expected_line2}', got '{lines[1]}'."

def test_source_files_modified():
    parser_src = "/home/user/src/parser.c"
    assert os.path.exists(parser_src), f"Source file {parser_src} missing."
    with open(parser_src, "r") as f:
        content = f.read()
    # Basic heuristic to ensure double-free is likely removed
    assert content.count("free(buf);") <= 1, "parser.c still appears to have a double-free (multiple free(buf); lines)."