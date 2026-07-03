# test_final_state.py

import os
import stat
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.exists(script_path), f"File {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_pipeline_script_no_python():
    script_path = "/home/user/pipeline.sh"
    with open(script_path, 'r') as f:
        content = f.read().lower()

    assert "python" not in content, "The script must not use Python."
    assert "perl" not in content, "The script must not use Perl."
    assert "ruby" not in content, "The script must not use Ruby."

def test_correlation_txt():
    corr_path = "/home/user/correlation.txt"
    assert os.path.exists(corr_path), f"File {corr_path} is missing."

    with open(corr_path, 'r') as f:
        content = f.read().strip()

    assert content == "0.998", f"Expected correlation to be '0.998', but got '{content}'"

def test_clean_data_csv():
    clean_data_path = "/home/user/clean_data.csv"
    assert os.path.exists(clean_data_path), f"File {clean_data_path} is missing."

    expected_content = """id,f1,f3,label
1,-1.000,4.000,0
2,-0.500,2.000,1
3,0.000,0.000,0
4,0.500,-2.000,1
5,1.000,-4.000,0"""

    with open(clean_data_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, "The contents of clean_data.csv do not match the expected output."