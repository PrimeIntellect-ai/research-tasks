import os
import json
import csv
import math
import pytest

def get_expected_results():
    """
    Recomputes the expected results based on the task description and initial data setup.
    Instead of using external libraries like pandas or numpy, we implement the logic
    using standard library modules to ensure independent verification.
    """
    initial_data_path = "/home/user/initial_data.csv"
    if not os.path.exists(initial_data_path):
        return None

    # Read initial data
    data = []
    with open(initial_data_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'x': float(row['x']),
                'y': float(row['y']),
                'value': float(row['value'])
            })

    # Sub-domains grouping
    subdomains = {i: [] for i in range(16)}
    for pt in data:
        i = min(int(pt['x'] * 4), 3)
        j = min(int(pt['y'] * 4), 3)
        idx = i * 4 + j
        subdomains[idx].append(pt['value'])

    # We can't perfectly replicate the numpy random sequence without numpy,
    # but the task explicitly mentions injecting high variance in subdomains 3 and 15.
    # We expect at least 3 and 15 to be refined.
    # For a robust test, we will check that the final point count matches 
    # the reported refined_subdomains length.

    return data

def test_files_exist():
    """Verify that the required output files exist."""
    assert os.path.exists("/home/user/refined_data.csv"), "refined_data.csv is missing"
    assert os.path.exists("/home/user/report.json"), "report.json is missing"

def test_report_structure_and_types():
    """Verify the structure and types of the JSON report."""
    report_path = "/home/user/report.json"
    if not os.path.exists(report_path):
        pytest.skip("report.json missing")

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not valid JSON")

    assert "refined_subdomains" in report, "Missing 'refined_subdomains' in report.json"
    assert isinstance(report["refined_subdomains"], list), "'refined_subdomains' must be a list"
    for item in report["refined_subdomains"]:
        assert isinstance(item, int), "Items in 'refined_subdomains' must be integers"

    assert "wasserstein_distance" in report, "Missing 'wasserstein_distance' in report.json"
    assert isinstance(report["wasserstein_distance"], (int, float)), "'wasserstein_distance' must be a float"

    assert "final_point_count" in report, "Missing 'final_point_count' in report.json"
    assert isinstance(report["final_point_count"], int), "'final_point_count' must be an integer"

def test_report_logic():
    """Verify that the report logic holds (counts match, known high-variance subdomains refined)."""
    report_path = "/home/user/report.json"
    if not os.path.exists(report_path):
        pytest.skip("report.json missing")

    with open(report_path, 'r') as f:
        report = json.load(f)

    refined_subdomains = report["refined_subdomains"]
    final_point_count = report["final_point_count"]

    # Check that it's sorted
    assert refined_subdomains == sorted(refined_subdomains), "'refined_subdomains' must be in ascending order"

    # Initial data has 400 points. Each refined subdomain adds 50 points.
    expected_count = 400 + 50 * len(refined_subdomains)
    assert final_point_count == expected_count, f"Expected final_point_count to be {expected_count}, got {final_point_count}"

    # Check that injected high variance domains (3 and 15) are in the refined list
    # Based on the setup script, these should definitely be flagged.
    assert 3 in refined_subdomains, "Subdomain 3 was expected to be refined due to injected high variance but is missing."
    assert 15 in refined_subdomains, "Subdomain 15 was expected to be refined due to injected high variance but is missing."

def test_refined_data_csv():
    """Verify the refined dataset CSV structure and row count."""
    csv_path = "/home/user/refined_data.csv"
    report_path = "/home/user/report.json"

    if not os.path.exists(csv_path) or not os.path.exists(report_path):
        pytest.skip("Required files missing")

    with open(report_path, 'r') as f:
        report = json.load(f)

    expected_count = report.get("final_point_count", 0)

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            pytest.fail("refined_data.csv is empty")

        assert header == ['x', 'y', 'value'], f"Expected header ['x', 'y', 'value'], got {header}"

        row_count = sum(1 for _ in reader)
        assert row_count == expected_count, f"refined_data.csv has {row_count} rows, expected {expected_count} based on report.json"