# test_final_state.py
import os
import csv
import re

def test_cleaned_logs_exists():
    assert os.path.exists("/home/user/data/cleaned_logs.csv"), "Cleaned logs file is missing."

def test_cleaned_logs_content():
    original_file = "/home/user/data/logs.csv"
    cleaned_file = "/home/user/data/cleaned_logs.csv"

    assert os.path.exists(original_file), "Original logs file is missing."
    assert os.path.exists(cleaned_file), "Cleaned logs file is missing."

    expected_rows = []
    with open(original_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        expected_rows.append(reader.fieldnames)
        for row in reader:
            rt_str = row['response_time']
            if rt_str == 'NA':
                rt_val = 250.0
                row['response_time'] = '250'
            else:
                rt_val = float(rt_str)
                if rt_val < 0 or rt_val > 5000:
                    continue
                # The awk script might leave it as is or format it, but conceptually it should match.
                # We'll just store the expected row as a dict for logical comparison.
            expected_rows.append(row)

    actual_rows = []
    with open(cleaned_file, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader)
        actual_rows.append(header)
        for row_list in reader:
            row_dict = dict(zip(header, row_list))
            actual_rows.append(row_dict)

    assert actual_rows[0] == expected_rows[0], "Header of cleaned_logs.csv is incorrect."

    # Compare row by row logically
    # Since the student might have formatted response_time differently (e.g., 250 vs 250.0),
    # we compare as floats where applicable.
    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, got {len(actual_rows)}."

    for i in range(1, len(expected_rows)):
        expected = expected_rows[i]
        actual = actual_rows[i]

        assert actual['id'] == expected['id'], f"Row {i}: ID mismatch."
        assert actual['message'] == expected['message'], f"Row {i}: Message mismatch."
        assert actual['is_anomaly'] == expected['is_anomaly'], f"Row {i}: is_anomaly mismatch."
        assert float(actual['response_time']) == float(expected['response_time']), f"Row {i}: response_time mismatch."

def test_metrics_file_format():
    metrics_file = "/home/user/metrics.txt"
    assert os.path.exists(metrics_file), "Metrics file is missing."

    with open(metrics_file, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) >= 2, "Metrics file should contain at least two lines."

    c_match = re.search(r"Best C:\s*([0-9.]+)", content[0])
    assert c_match, "First line must match 'Best C: <value>'."
    c_val = float(c_match.group(1))
    assert c_val in [0.01, 0.1, 1.0, 10.0], f"Best C value {c_val} is not in the expected grid."

    score_match = re.search(r"Best CV Score:\s*([0-9.]+)", content[1])
    assert score_match, "Second line must match 'Best CV Score: <score>'."
    score_str = score_match.group(1)

    # Check if it's rounded to 4 decimal places
    if '.' in score_str:
        decimals = len(score_str.split('.')[1])
        assert decimals <= 4, "CV Score should be rounded to 4 decimal places."