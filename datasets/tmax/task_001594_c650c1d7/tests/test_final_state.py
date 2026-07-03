# test_final_state.py
import os

def test_etl_go_exists():
    etl_path = "/home/user/etl.go"
    assert os.path.exists(etl_path), f"The Go program file {etl_path} does not exist."
    assert os.path.isfile(etl_path), f"{etl_path} is not a file."

def test_output_csv_exists_and_content():
    output_path = "/home/user/output.csv"
    assert os.path.exists(output_path), f"The output file {output_path} does not exist. Did you run your Go program?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    expected_csv = """ts,id,temp_c,rolling_avg_temp_c
100,S1,27.00,27.00
102,S1,30.00,28.50
104,S2,17.00,24.67
106,S1,10.00,19.00
108,S4,40.00,22.33"""

    with open(output_path, "r") as f:
        actual_content = f.read().strip()

    # Normalize line endings to avoid issues with \r\n vs \n
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_csv.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The content of {output_path} does not match the expected output.\n"
        f"Expected:\n{expected_csv}\n\nActual:\n{actual_content}"
    )