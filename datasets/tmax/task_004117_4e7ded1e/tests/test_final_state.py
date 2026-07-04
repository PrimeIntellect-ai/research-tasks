# test_final_state.py

import os
import csv
from collections import defaultdict

def test_utf8_sales_csv_exists_and_is_utf8():
    """Verify that the utf8_sales.csv file exists and is correctly encoded in UTF-8."""
    file_path = "/home/user/utf8_sales.csv"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

    # Verify it can be read as UTF-8
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except UnicodeDecodeError:
        assert False, f"File {file_path} is not valid UTF-8."

    assert "StoreID,Date,SalesAmount,Currency" in content, "Header is missing or incorrect in utf8_sales.csv."
    assert "£" in content, "Special characters were lost or corrupted during conversion."

def test_c_program_exists():
    """Verify that the C program source file exists."""
    file_path = "/home/user/process_sales.c"
    assert os.path.exists(file_path), f"File {file_path} is missing."
    assert os.path.isfile(file_path), f"Path {file_path} is not a file."

def test_rolling_sales_csv_content():
    """Verify that the rolling_sales.csv file contains the correct calculated statistics."""
    raw_file_path = "/home/user/raw_sales.csv"
    output_file_path = "/home/user/rolling_sales.csv"

    assert os.path.exists(output_file_path), f"File {output_file_path} is missing."

    # Compute expected output dynamically from the original raw file
    data_by_store = defaultdict(list)
    with open(raw_file_path, "r", encoding="iso-8859-1") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data_by_store[row["StoreID"]].append({
                "Date": row["Date"],
                "SalesAmount": float(row["SalesAmount"])
            })

    expected_rows = []
    for store_id in sorted(data_by_store.keys()):
        # Sort by date
        store_data = sorted(data_by_store[store_id], key=lambda x: x["Date"])

        for i, record in enumerate(store_data):
            # 3-day rolling window: current day + up to 2 preceding days
            start_idx = max(0, i - 2)
            window = store_data[start_idx:i+1]
            rolling_avg = sum(item["SalesAmount"] for item in window) / len(window)

            expected_rows.append({
                "StoreID": store_id,
                "Date": record["Date"],
                "SalesAmount": f"{record['SalesAmount']:.2f}",
                "RollingAvg": f"{rolling_avg:.2f}"
            })

    # Read actual output
    actual_rows = []
    with open(output_file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["StoreID", "Date", "SalesAmount", "RollingAvg"], "Output CSV header is incorrect."
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), "Output CSV does not have the correct number of rows."

    for i, (expected, actual) in enumerate(zip(expected_rows, actual_rows)):
        assert actual["StoreID"] == expected["StoreID"], f"Row {i+1}: Expected StoreID {expected['StoreID']}, got {actual['StoreID']}."
        assert actual["Date"] == expected["Date"], f"Row {i+1}: Expected Date {expected['Date']}, got {actual['Date']}."
        assert actual["SalesAmount"] == expected["SalesAmount"], f"Row {i+1}: Expected SalesAmount {expected['SalesAmount']}, got {actual['SalesAmount']}."
        assert actual["RollingAvg"] == expected["RollingAvg"], f"Row {i+1}: Expected RollingAvg {expected['RollingAvg']}, got {actual['RollingAvg']}."