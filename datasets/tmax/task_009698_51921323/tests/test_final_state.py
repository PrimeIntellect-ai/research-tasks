# test_final_state.py

import os
import pytest

def test_output_file_exists_and_content():
    output_file = "/home/user/loc_summary.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing. Did you run the Rust script?"

    expected_content = """hour_bucket,loc_key,unique_masked_ips,avg_conf
3600,BTN_CANCEL,1,95
3600,BTN_OK,2,85
7200,BTN_OK,2,95"""

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == expected_content, f"Content of {output_file} does not match expected output.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_rust_script_exists():
    script_file = "/home/user/etl_fix.rs"
    assert os.path.isfile(script_file), f"Rust script {script_file} is missing."