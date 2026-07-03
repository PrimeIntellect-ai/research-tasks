# test_final_state.py
import os

def test_output_csv_correct():
    output_path = "/home/user/etl_pipeline/output.csv"
    assert os.path.isfile(output_path), f"File {output_path} does not exist. Did you run the filter program?"

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "id,value",
        "20000001,50.5",
        "20000003,99.9",
        "20000004,25.0"
    ]

    assert lines == expected_lines, f"Output CSV content is incorrect.\nExpected: {expected_lines}\nGot: {lines}"

def test_validation_log_pass():
    log_path = "/home/user/etl_pipeline/validation.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist. Did you run the validation script?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert "PASS" in content, f"validation.log does not contain 'PASS'. Actual content:\n{content}"

def test_filter_c_fixed():
    src_path = "/home/user/etl_pipeline/filter.c"
    assert os.path.isfile(src_path), f"File {src_path} does not exist."

    with open(src_path, "r") as f:
        content = f.read()

    assert "float id_float;" not in content, "filter.c still contains the buggy 'float id_float;' declaration. You must fix the precision loss issue."
    assert "sscanf" in content, "filter.c should still use sscanf to parse the line, but correctly."

def test_executable_compiled():
    exe_path = "/home/user/etl_pipeline/filter"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did you run 'make'?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."