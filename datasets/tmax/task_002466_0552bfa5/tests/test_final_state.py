# test_final_state.py

import os
import stat

def test_etl_script_exists_and_executable():
    script_path = "/home/user/etl.sh"
    assert os.path.exists(script_path), f"Script missing: {script_path}"
    assert os.path.isfile(script_path), f"Path is not a file: {script_path}"

    # Check if executable by owner, group, or others
    st = os.stat(script_path)
    is_executable = bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))
    assert is_executable, f"Script is not executable: {script_path}"

def test_processed_csv_content():
    output_path = "/home/user/processed.csv"
    assert os.path.exists(output_path), f"Output file missing: {output_path}"
    assert os.path.isfile(output_path), f"Path is not a file: {output_path}"

    expected_content = [
        "u101,premium,12,LowRisk",
        "u102,basic,4,HighRisk",
        "u104,premium,8,LowRisk",
        "u106,basic,3,HighRisk",
        "u107,enterprise,25,LowRisk"
    ]

    with open(output_path, "r") as f:
        # Read lines, strip whitespace/newlines, filter out empty lines
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_content, (
        f"Content of {output_path} does not match expected.\n"
        f"Expected:\n{chr(10).join(expected_content)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )