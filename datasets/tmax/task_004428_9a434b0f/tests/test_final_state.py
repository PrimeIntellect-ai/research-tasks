# test_final_state.py

import os
import stat
import pytest

def test_extract_script_exists():
    path = "/home/user/extract.py"
    assert os.path.exists(path), f"Expected script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

def test_pipeline_script_exists_and_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.exists(path), f"Expected script {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    # Check if executable
    st = os.stat(path)
    assert st.st_mode & stat.S_IXUSR, f"{path} is not executable by the owner."

def test_clean_data_csv_content():
    path = "/home/user/clean_data.csv"
    assert os.path.exists(path), f"Expected output file {path} does not exist."
    assert os.path.isfile(path), f"{path} is not a file."

    expected_lines = [
        "2022-12-31 23:59:59,new_year@party.org",
        "2023-10-14 08:30:00,admin@server.local",
        "2023-10-15 09:15:22,root@localhost",
        "2023-10-16 11:11:11,user.test@enterprise.com"
    ]

    with open(path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The content of {path} does not match the expected final output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )