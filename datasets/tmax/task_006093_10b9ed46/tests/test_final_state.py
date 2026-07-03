# test_final_state.py

import os
import pytest

def test_valid_changes_tsv():
    tsv_path = "/home/user/valid_changes.tsv"
    assert os.path.isfile(tsv_path), f"{tsv_path} does not exist."

    expected_lines = [
        "DB_HOST\tlocalhost\ta_init.conf",
        "DB_PASS\tS3cr3t\td_override.conf",
        "GREETING\t¡Hola Mundo!\tb_update.conf",
        "MAX_CONN\t500\td_override.conf",
        "SERVER_PORT\t9000\tb_update.conf",
        "WELCOME_MSG\tHello World\ta_init.conf"
    ]

    with open(tsv_path, "r", encoding="utf-8") as f:
        # Strip newlines for comparison, ignore empty lines
        actual_lines = [line.strip('\n') for line in f if line.strip('\n')]

    assert actual_lines == expected_lines, (
        f"Content of {tsv_path} does not match the expected output.\n"
        f"Expected:\n{expected_lines}\n"
        f"Actual:\n{actual_lines}"
    )

def test_tracker_cpp_concurrency():
    cpp_path = "/home/user/tracker.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."

    with open(cpp_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Check for concurrency keywords
    concurrency_keywords = ["std::thread", "async", "execution::par", "pthread"]
    has_concurrency = any(kw in content for kw in concurrency_keywords)

    assert has_concurrency, (
        "tracker.cpp does not appear to use std::thread, std::async, "
        "or C++17 parallel algorithms (execution::par) as required."
    )

def test_run_pipeline_sh():
    sh_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(sh_path), f"{sh_path} does not exist."