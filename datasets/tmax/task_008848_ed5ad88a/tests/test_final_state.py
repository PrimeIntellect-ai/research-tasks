# test_final_state.py
import os
import csv

def test_leak_report_exists_and_correct():
    train_file = "/home/user/train_data.csv"
    test_file = "/home/user/test_data.csv"
    report_file = "/home/user/leak_report.csv"

    assert os.path.isfile(report_file), f"Missing output file: {report_file}"

    # Read train data
    train_data = {}
    with open(train_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 4:
                train_data[row[1]] = float(row[3])

    # Read test data
    test_data = {}
    with open(test_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 4:
                test_data[row[1]] = float(row[3])

    # Compute expected results
    expected_results = []
    for f_hash, train_conf in train_data.items():
        if f_hash in test_data:
            test_conf = test_data[f_hash]
            diff = abs(train_conf - test_conf)
            expected_results.append((f_hash, diff))

    # Sort: descending by diff, ascending by feature_hash
    expected_results.sort(key=lambda x: (-x[1], x[0]))

    expected_lines = [f"{f_hash},{diff:.3f}" for f_hash, diff in expected_results]
    expected_content = "\n".join(expected_lines) + "\n"

    with open(report_file, "r") as f:
        actual_content = f.read()

    # Normalize newlines for comparison
    actual_lines = [line.strip() for line in actual_content.strip().split("\n") if line.strip()]
    expected_lines_stripped = [line.strip() for line in expected_content.strip().split("\n") if line.strip()]

    assert actual_lines == expected_lines_stripped, (
        f"Content of {report_file} does not match expected output.\n"
        f"Expected:\n{chr(10).join(expected_lines_stripped)}\n"
        f"Actual:\n{chr(10).join(actual_lines)}"
    )