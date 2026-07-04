# test_final_state.py

import os
import stat

def test_process_logs_script_exists_and_executable():
    script_path = "/home/user/process_logs.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"Path {script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"Script {script_path} is not executable."

def test_processed_logs_csv_content():
    csv_path = "/home/user/processed_logs.csv"
    assert os.path.exists(csv_path), f"Output file {csv_path} does not exist. Did you run your script?"
    assert os.path.isfile(csv_path), f"Path {csv_path} is not a file."

    expected_lines = [
        "timestamp,service,status,rolling_avg",
        "2023-10-01T10:00:01,auth,200,200",
        "2023-10-01T10:00:02,auth,500,350",
        "2023-10-01T10:00:03,auth,200,300",
        "2023-10-01T10:00:04,auth,503,401",
        "2023-10-01T10:00:05,db,200,200",
        "2023-10-01T10:00:06,db,404,302",
        "2023-10-01T10:00:08,db,200,268",
        "2023-10-01T10:00:09,db,200,268"
    ]

    with open(csv_path, "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in {csv_path}, but found {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} in {csv_path} does not match expected output.\nExpected: {expected}\nActual: {actual.strip()}"