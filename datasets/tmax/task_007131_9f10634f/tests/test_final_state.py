# test_final_state.py
import os
import pytest

def test_processor_c_exists():
    path = "/home/user/processor.c"
    assert os.path.isfile(path), f"File {path} is missing."
    with open(path, "r") as f:
        content = f.read()
    assert "#include" in content, f"{path} does not look like valid C code."

def test_processor_executable_exists():
    path = "/home/user/processor"
    assert os.path.isfile(path), f"Compiled executable {path} is missing."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_run_pipeline_sh_exists_and_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Script {path} is missing."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

def test_backup_report_txt_content():
    path = "/home/user/backup_report.txt"
    assert os.path.isfile(path), f"Report file {path} is missing."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[2023-10-01] users_db::profiles",
        "[2023-10-02] orders_db::transactions",
        "[2023-10-03] users_db::profiles"
    ]

    assert sorted(lines) == sorted(expected_lines), f"Content of {path} does not match the expected output."