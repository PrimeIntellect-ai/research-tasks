# test_final_state.py

import os
import csv
import math

def get_expected_results(csv_path):
    if not os.path.exists(csv_path):
        return None

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    complete_rows = []
    for row in rows:
        raw = row['raw_value'].strip()
        pred = row['model_prediction'].strip()
        if raw in ('', 'NaN', 'NULL') or pred in ('', 'NaN', 'NULL'):
            continue
        complete_rows.append((float(raw), float(pred)))

    initial_complete_rows = len(complete_rows)

    if initial_complete_rows == 0:
        return initial_complete_rows, 0, 0.0, 0

    mean_raw = sum(r[0] for r in complete_rows) / initial_complete_rows
    variance = sum((r[0] - mean_raw) ** 2 for r in complete_rows) / initial_complete_rows
    std_dev = math.sqrt(variance)

    upper_bound = mean_raw + 2 * std_dev
    lower_bound = mean_raw - 2 * std_dev

    clean_rows = []
    outliers_removed = 0
    for r in complete_rows:
        if r[0] > upper_bound or r[0] < lower_bound:
            outliers_removed += 1
        else:
            clean_rows.append(r)

    if not clean_rows:
        return initial_complete_rows, outliers_removed, 0.0, 0

    clean_mean = sum(r[0] for r in clean_rows) / len(clean_rows)
    # The prompt asks to round to exactly 2 decimal places
    clean_mean_str = f"{clean_mean:.2f}"

    failed_validation = sum(1 for r in clean_rows if abs(r[0] - r[1]) > 0.5)

    return initial_complete_rows, outliers_removed, clean_mean_str, failed_validation

def test_analysis_report_exists():
    """Test that the analysis_report.txt file was created."""
    assert os.path.isfile('/home/user/analysis_report.txt'), "The file /home/user/analysis_report.txt does not exist."

def test_analysis_report_content():
    """Test that the analysis_report.txt file contains the correctly calculated metrics."""
    csv_path = '/home/user/model_outputs.csv'
    assert os.path.isfile(csv_path), f"Required data file {csv_path} is missing."

    results = get_expected_results(csv_path)
    assert results is not None, "Failed to compute expected results."

    initial_complete_rows, outliers_removed, clean_mean_str, failed_validation = results

    expected_content = (
        f"Initial Complete Rows: {initial_complete_rows}\n"
        f"Outliers Removed: {outliers_removed}\n"
        f"Clean Mean Raw: {clean_mean_str}\n"
        f"Failed Validation: {failed_validation}"
    )

    report_path = '/home/user/analysis_report.txt'
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The contents of {report_path} are incorrect.\n"
        f"Expected:\n{expected_content}\n\n"
        f"Got:\n{actual_content}"
    )