# test_final_state.py

import os
import hashlib

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def test_clean_data_exists_and_correct():
    clean_data_path = "/home/user/clean_data.csv"
    assert os.path.isfile(clean_data_path), f"Output file {clean_data_path} does not exist."

    expected_clean = "id,value,score\n1,10.5,80\n5,3.14,100\n6,42.0,85\n9,99.9,10\n"

    with open(clean_data_path, "r") as f:
        clean_data = f.read()

    # Check lines ignoring trailing newlines differences
    assert clean_data.strip() == expected_clean.strip(), f"Content of {clean_data_path} does not match expected output. Ensure filtering logic is correct."

def test_experiments_log_correct():
    raw_data_path = "/home/user/raw_data.csv"
    clean_data_path = "/home/user/clean_data.csv"
    log_path = "/home/user/experiments.log"

    assert os.path.isfile(raw_data_path), f"Input file {raw_data_path} is missing."
    assert os.path.isfile(clean_data_path), f"Output file {clean_data_path} is missing."
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    in_hash = md5(raw_data_path)
    out_hash = md5(clean_data_path)

    with open(clean_data_path, "r") as f:
        lines = f.readlines()
    line_count = len(lines)

    expected_log = f"IN:{in_hash} OUT:{out_hash} LINES:{line_count}"

    with open(log_path, "r") as f:
        log_data = f.read()

    assert expected_log in log_data, f"experiments.log does not contain the correct tracking string. Expected to find: '{expected_log}'"

def test_script_exists():
    script_path = "/home/user/clean_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."