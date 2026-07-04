# test_final_state.py

import os
import subprocess
import csv
import pytest

GO_FILE_PATH = "/home/user/generate_report.go"
CSV_FILE_PATH = "/home/user/report.csv"
DB_PATH = "/home/user/ecommerce.db"
WORKSPACE = "/home/user"

def test_go_file_exists():
    assert os.path.exists(GO_FILE_PATH), f"Go source file not found at {GO_FILE_PATH}"
    assert os.path.isfile(GO_FILE_PATH), f"Path {GO_FILE_PATH} is not a file"

def run_go_program(region, limit):
    # Remove existing CSV to ensure we test the newly generated one
    if os.path.exists(CSV_FILE_PATH):
        os.remove(CSV_FILE_PATH)

    cmd = ["go", "run", "generate_report.go", "-region", region, "-limit", str(limit)]
    result = subprocess.run(cmd, cwd=WORKSPACE, capture_output=True, text=True)

    assert result.returncode == 0, f"Go program failed to run.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert os.path.exists(CSV_FILE_PATH), f"CSV file was not created at {CSV_FILE_PATH} after running the program"

def read_csv():
    with open(CSV_FILE_PATH, 'r', newline='') as f:
        reader = csv.reader(f)
        return list(reader)

def test_go_program_output_north_america_limit_2():
    run_go_program("North America", 2)

    rows = read_csv()
    assert len(rows) > 0, "CSV file is empty"

    header = rows[0]
    expected_header = ["name", "total_spend", "rank", "running_total"]
    assert header == expected_header, f"Expected header {expected_header}, but got {header}"

    assert len(rows) == 3, f"Expected 1 header + 2 data rows, but got {len(rows)} total rows"

    # Check data types and values
    # Alice, 600, 1, 600
    assert rows[1][0] == "Alice", f"Expected rank 1 name 'Alice', got '{rows[1][0]}'"
    assert float(rows[1][1]) == 600.0, f"Expected Alice total_spend 600, got '{rows[1][1]}'"
    assert int(rows[1][2]) == 1, f"Expected Alice rank 1, got '{rows[1][2]}'"
    assert float(rows[1][3]) == 600.0, f"Expected Alice running_total 600, got '{rows[1][3]}'"

    # Charlie, 300, 2, 900
    assert rows[2][0] == "Charlie", f"Expected rank 2 name 'Charlie', got '{rows[2][0]}'"
    assert float(rows[2][1]) == 300.0, f"Expected Charlie total_spend 300, got '{rows[2][1]}'"
    assert int(rows[2][2]) == 2, f"Expected Charlie rank 2, got '{rows[2][2]}'"
    assert float(rows[2][3]) == 900.0, f"Expected Charlie running_total 900, got '{rows[2][3]}'"

def test_go_program_output_north_america_limit_3():
    run_go_program("North America", 3)

    rows = read_csv()
    assert len(rows) == 4, f"Expected 1 header + 3 data rows, but got {len(rows)} total rows"

    # Bob, 150, 3, 1050
    assert rows[3][0] == "Bob", f"Expected rank 3 name 'Bob', got '{rows[3][0]}'"
    assert float(rows[3][1]) == 150.0, f"Expected Bob total_spend 150, got '{rows[3][1]}'"
    assert int(rows[3][2]) == 3, f"Expected Bob rank 3, got '{rows[3][2]}'"
    assert float(rows[3][3]) == 1050.0, f"Expected Bob running_total 1050, got '{rows[3][3]}'"

def test_go_program_output_europe_limit_1():
    run_go_program("Europe", 1)

    rows = read_csv()
    assert len(rows) == 2, f"Expected 1 header + 1 data row, but got {len(rows)} total rows"

    # Diana, 1000, 1, 1000
    assert rows[1][0] == "Diana", f"Expected rank 1 name 'Diana', got '{rows[1][0]}'"
    assert float(rows[1][1]) == 1000.0, f"Expected Diana total_spend 1000, got '{rows[1][1]}'"
    assert int(rows[1][2]) == 1, f"Expected Diana rank 1, got '{rows[1][2]}'"
    assert float(rows[1][3]) == 1000.0, f"Expected Diana running_total 1000, got '{rows[1][3]}'"