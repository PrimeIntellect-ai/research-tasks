# test_final_state.py

import os
import pytest

def test_c_source_and_executable_exist():
    c_source = "/home/user/etl_step.c"
    executable = "/home/user/etl_step"

    assert os.path.isfile(c_source), f"C source file {c_source} is missing."
    assert os.path.isfile(executable), f"Executable file {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_report_content():
    corpus_path = "/home/user/corpus.txt"
    template_path = "/home/user/report.tmpl"
    report_path = "/home/user/report.txt"

    assert os.path.isfile(corpus_path), f"Input file {corpus_path} is missing."
    assert os.path.isfile(template_path), f"Template file {template_path} is missing."
    assert os.path.isfile(report_path), f"Output file {report_path} is missing."

    # Compute expected statistics
    with open(corpus_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    total_words = 0
    max_len = 0

    for line in lines:
        # split() without arguments splits by all whitespace, matching the C requirement
        # for standard ASCII whitespace (space, tab, newline).
        words = line.split()
        total_words += len(words)
        for word in words:
            if len(word) > max_len:
                max_len = len(word)

    # Generate expected report
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()

    expected_report = template_content.replace("{{LINES}}", str(total_lines))
    expected_report = expected_report.replace("{{WORDS}}", str(total_words))
    expected_report = expected_report.replace("{{MAX_LEN}}", str(max_len))

    # Read actual report
    with open(report_path, "r", encoding="utf-8") as f:
        actual_report = f.read()

    assert actual_report == expected_report, (
        f"Content of {report_path} does not match expected output.\n"
        f"Expected:\n{expected_report}\n"
        f"Actual:\n{actual_report}"
    )