# test_final_state.py

import os
import stat
import pytest

def test_pipeline_script_exists_and_executable():
    """Verify that the pipeline script exists and is executable."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_cpp_processor_exists():
    """Verify that the C++ source file exists."""
    cpp_path = "/home/user/processor.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."

def test_clean_data_content():
    """Verify that clean_data.csv was created and filtered correctly."""
    clean_path = "/home/user/clean_data.csv"
    assert os.path.isfile(clean_path), f"{clean_path} does not exist."

    with open(clean_path, 'r') as f:
        lines = f.read().strip().split('\n')

    for line in lines:
        if not line.strip():
            continue
        assert not line.startswith("id,category"), "clean_data.csv should not contain the header."
        cols = line.split(',')
        if len(cols) > 1:
            assert cols[1] != "IGNORE", "clean_data.csv should not contain rows with category IGNORE."

def test_final_output_content():
    """Verify the final output matches the expected result."""
    output_path = "/home/user/final_output.csv"
    assert os.path.isfile(output_path), f"{output_path} does not exist."

    expected_lines = [
        "id,category,distance",
        "u4,A,0.000",
        "u1,A,2.000",
        "u3,B,5.500",
        "u7,B,9.000",
        "u9,C,0.000",
        "u6,C,5.000"
    ]

    with open(output_path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, f"Content of {output_path} is incorrect. Expected: {expected_lines}, but got: {actual_lines}"