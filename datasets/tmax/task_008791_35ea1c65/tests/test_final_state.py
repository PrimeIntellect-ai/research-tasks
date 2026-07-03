# test_final_state.py
import os
import csv
from collections import defaultdict

def test_files_exist():
    workspace = "/home/user/workspace"

    copied_csv = os.path.join(workspace, "sales_wide.csv")
    assert os.path.isfile(copied_csv), f"Expected {copied_csv} to exist (task: copy the file)."

    source_file = os.path.join(workspace, "process.c")
    assert os.path.isfile(source_file), f"Expected C source code at {source_file}."

    executable = os.path.join(workspace, "process")
    assert os.path.isfile(executable), f"Expected compiled executable at {executable}."

    summary_file = os.path.join(workspace, "summary.csv")
    assert os.path.isfile(summary_file), f"Expected output file at {summary_file}."

def test_summary_csv_content():
    staging_csv = "/home/user/staging/sales_wide.csv"
    assert os.path.isfile(staging_csv), f"Original data file {staging_csv} is missing."

    # Recompute the expected output
    sums = defaultdict(int)
    with open(staging_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            region = row['Region']
            for q in ['Q1', 'Q2', 'Q3', 'Q4']:
                val = int(row[q])
                if val >= 0:
                    sums[region] += val

    sorted_sums = sorted(sums.items(), key=lambda x: x[1], reverse=True)

    expected_lines = ["Region,TotalSum"]
    for region, total in sorted_sums:
        expected_lines.append(f"{region},{total}")

    expected_content = "\n".join(expected_lines)

    summary_file = "/home/user/workspace/summary.csv"
    with open(summary_file, 'r') as f:
        actual_content = f.read().strip()

    # Normalize line endings
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines_normalized = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines_normalized, (
        "The content of summary.csv does not match the expected aggregated and sorted output.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )