# test_final_state.py
import os
import csv
import math

def get_expected_correlation(csv_path):
    n = 0
    sum_x = 0.0
    sum_y = 0.0
    sum_xy = 0.0
    sum_x2 = 0.0
    sum_y2 = 0.0

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row:
                continue
            if float(row[3]) > 50.0:
                x = float(row[1])
                y = float(row[2])
                sum_x += x
                sum_y += y
                sum_xy += x * y
                sum_x2 += x * x
                sum_y2 += y * y
                n += 1

    if n == 0:
        return "0.0000"

    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y))
    if denominator == 0:
        return "0.0000"
    return f"{numerator / denominator:.4f}"

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_result_txt_content():
    csv_path = "/home/user/data/benchmarks.csv"
    result_path = "/home/user/result.txt"

    assert os.path.isfile(csv_path), f"Data file {csv_path} is missing."
    assert os.path.isfile(result_path), f"Result file {result_path} does not exist."

    expected_val = get_expected_correlation(csv_path)

    with open(result_path, 'r') as f:
        actual_val = f.read().strip()

    assert actual_val == expected_val, f"Expected correlation {expected_val}, but found {actual_val} in {result_path}."