# test_final_state.py

import os
import stat
import pytest

def test_validate_c_and_executable():
    c_path = "/home/user/validate.c"
    exe_path = "/home/user/validate"

    assert os.path.exists(c_path), f"File {c_path} is missing."
    assert os.path.exists(exe_path), f"File {exe_path} is missing."

    st = os.stat(exe_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{exe_path} is not executable."

def test_pipeline_sh_exists_and_contains_keywords():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"File {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    assert "gcc" in content, "pipeline.sh does not contain 'gcc' command."
    assert "&" in content, "pipeline.sh does not use '&' for background tasks."
    assert "wait" in content, "pipeline.sh does not contain 'wait' command."

def test_processed_valid_csv():
    file_path = "/home/user/processed_valid.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    expected_valid = {
        "1612345678,alice,US,max_conn,MOD,100",
        "1612345679,bob,US,timeout,ADD,30",
        "1612345680,dave,US,port,DEL,",
        "1612345681,eve,EU,host,MOD,localhost",
        "1612345684,heidi,EU,ssl,ADD,true",
        "1612345686,judy,AP,log,MOD,debug"
    }

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 6, f"Expected 6 valid lines, got {len(lines)}."
    assert set(lines) == expected_valid, "Content of processed_valid.csv does not match expected valid lines."

def test_processed_invalid_csv():
    file_path = "/home/user/processed_invalid.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    expected_invalid = {
        "1500000000,charlie,US,retry,MOD,5",
        "1612345682,frank,EU,user,UPDATE,admin",
        "1612345683,grace,E,pass,MOD,secret",
        "1612345685,,AP,cache,MOD,1"
    }

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 invalid lines, got {len(lines)}."
    assert set(lines) == expected_invalid, "Content of processed_invalid.csv does not match expected invalid lines."

def test_stats_txt():
    file_path = "/home/user/stats.txt"
    assert os.path.exists(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_stats = "Total Valid: 6\nTotal Invalid: 4"
    assert content == expected_stats, f"Content of stats.txt is incorrect. Expected:\n{expected_stats}\nGot:\n{content}"