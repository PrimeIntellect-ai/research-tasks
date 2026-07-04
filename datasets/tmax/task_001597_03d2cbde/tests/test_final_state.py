# test_final_state.py
import os
import subprocess
import csv

SCRIPT_PATH = "/home/user/report.sh"

def run_script(args):
    return subprocess.run([SCRIPT_PATH] + args, capture_output=True, text=True)

def check_csv_content(file_path, expected_rows):
    with open(file_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "CSV file is empty"
    assert rows[0] == expected_rows[0], f"Header mismatch. Expected {expected_rows[0]}, got {rows[0]}"
    assert len(rows) == len(expected_rows), f"Row count mismatch. Expected {len(expected_rows)} rows, got {len(rows)}"

    for i in range(1, len(rows)):
        assert rows[i][0] == expected_rows[i][0], f"Row {i} Employee mismatch. Expected {expected_rows[i][0]}, got {rows[i][0]}"
        assert rows[i][1] == expected_rows[i][1], f"Row {i} Department mismatch. Expected {expected_rows[i][1]}, got {rows[i][1]}"
        assert float(rows[i][2]) == float(expected_rows[i][2]), f"Row {i} TotalSales mismatch. Expected {expected_rows[i][2]}, got {rows[i][2]}"
        assert int(rows[i][3]) == int(expected_rows[i][3]), f"Row {i} DeptRank mismatch. Expected {expected_rows[i][3]}, got {rows[i][3]}"

def test_report_sh_exists_and_executable():
    assert os.path.exists(SCRIPT_PATH), f"{SCRIPT_PATH} is missing"
    assert os.access(SCRIPT_PATH, os.X_OK), f"{SCRIPT_PATH} is not executable"

def test_report_all_departments():
    out_file = "/home/user/out_all.csv"
    if os.path.exists(out_file):
        os.remove(out_file)

    res = run_script(["ALL", "10", "0", out_file])
    assert res.returncode == 0, f"Script failed with error: {res.stderr}"
    assert os.path.exists(out_file), f"Output file {out_file} was not created"

    expected = [
        ["Employee", "Department", "TotalSales", "DeptRank"],
        ["Eve", "Clothing", "450.0", "1"],
        ["David", "Clothing", "150.0", "2"],
        ["Bob", "Electronics", "1000.0", "1"],
        ["Alice", "Electronics", "800.0", "2"],
        ["Charlie", "Electronics", "200.0", "3"],
        ["Frank", "Home", "900.0", "1"]
    ]

    check_csv_content(out_file, expected)

def test_report_specific_department_with_pagination():
    out_file = "/home/user/out_dept1.csv"
    if os.path.exists(out_file):
        os.remove(out_file)

    res = run_script(["1", "2", "1", out_file])
    assert res.returncode == 0, f"Script failed with error: {res.stderr}"
    assert os.path.exists(out_file), f"Output file {out_file} was not created"

    expected = [
        ["Employee", "Department", "TotalSales", "DeptRank"],
        ["Alice", "Electronics", "800.0", "2"],
        ["Charlie", "Electronics", "200.0", "3"]
    ]

    check_csv_content(out_file, expected)