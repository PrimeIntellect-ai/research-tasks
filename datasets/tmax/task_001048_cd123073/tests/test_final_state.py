# test_final_state.py
import os

def test_etl_fixed_executable():
    exe_path = "/home/user/etl_fixed"
    assert os.path.exists(exe_path), f"Missing executable: {exe_path}"
    assert os.path.isfile(exe_path), f"{exe_path} is not a file"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable"

def test_data_clean_csv():
    clean_csv = "/home/user/data_clean.csv"
    assert os.path.exists(clean_csv), f"Missing file: {clean_csv}"

    with open(clean_csv, "r") as f:
        content = f.read().strip()

    expected_content = """id,timestamp
1,1600000000
2,1600000001
3,3000000000
4,4000000000
5,500000000000"""

    assert content == expected_content, "The content of data_clean.csv does not match the expected output. Large timestamps may still be overflowing."