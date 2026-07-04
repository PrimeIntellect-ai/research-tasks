# test_final_state.py

import os
import pytest

def test_output_files_exist():
    train_path = "/home/user/etl_pipeline/output_train.csv"
    test_path = "/home/user/etl_pipeline/output_test.csv"

    assert os.path.isfile(train_path), f"Expected output file {train_path} does not exist. Did you run `cargo run`?"
    assert os.path.isfile(test_path), f"Expected output file {test_path} does not exist. Did you run `cargo run`?"

def test_output_test_csv_content():
    test_path = "/home/user/etl_pipeline/output_test.csv"
    with open(test_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected 3 lines in output_test.csv (1 header, 2 data rows), but got {len(lines)}"

    expected_header = "id,scaled_value,fast,hello,is,rust,world"
    assert lines[0] == expected_header, f"Header in output_test.csv is incorrect. Expected '{expected_header}', got '{lines[0]}'"

    expected_row_4 = "4,8.0000,0,1,0,0,0"
    assert lines[1] == expected_row_4, f"Row 4 in output_test.csv is incorrect. Expected '{expected_row_4}', got '{lines[1]}'"

    expected_row_5 = "5,9.0000,1,0,0,0,0"
    assert lines[2] == expected_row_5, f"Row 5 in output_test.csv is incorrect. Expected '{expected_row_5}', got '{lines[2]}'"

def test_output_train_csv_content():
    train_path = "/home/user/etl_pipeline/output_train.csv"
    with open(train_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 4, f"Expected 4 lines in output_train.csv (1 header, 3 data rows), but got {len(lines)}"

    expected_header = "id,scaled_value,fast,hello,is,rust,world"
    assert lines[0] == expected_header, f"Header in output_train.csv is incorrect. Expected '{expected_header}', got '{lines[0]}'"

    expected_row_1 = "1,-1.0000,0,1,0,0,1"
    assert lines[1] == expected_row_1, f"Row 1 in output_train.csv is incorrect. Expected '{expected_row_1}', got '{lines[1]}'"

    expected_row_2 = "2,0.0000,0,1,0,1,0"
    assert lines[2] == expected_row_2, f"Row 2 in output_train.csv is incorrect. Expected '{expected_row_2}', got '{lines[2]}'"

    expected_row_3 = "3,1.0000,1,0,1,1,0"
    assert lines[3] == expected_row_3, f"Row 3 in output_train.csv is incorrect. Expected '{expected_row_3}', got '{lines[3]}'"