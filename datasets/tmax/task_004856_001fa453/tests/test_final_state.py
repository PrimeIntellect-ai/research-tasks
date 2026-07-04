# test_final_state.py
import os
import json
import pytest

def test_report_exists():
    """Verify that the report.json file was generated in the correct directory."""
    report_path = "/home/user/etl_transform/report.json"
    assert os.path.exists(report_path), f"Expected report file not found at {report_path}"
    assert os.path.isfile(report_path), f"Expected a file, but found a directory at {report_path}"

def test_report_structure_and_accuracy():
    """Verify the JSON structure, accuracy_passed value, and eigenvalues."""
    report_path = "/home/user/etl_transform/report.json"
    if not os.path.exists(report_path):
        pytest.fail(f"Cannot test structure because {report_path} does not exist.")

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    assert "accuracy_passed" in report_data, "JSON missing 'accuracy_passed' key."
    assert "eigenvalues" in report_data, "JSON missing 'eigenvalues' key."

    assert report_data["accuracy_passed"] is True, "Expected 'accuracy_passed' to be true."

    computed_eigenvalues = report_data["eigenvalues"]
    assert isinstance(computed_eigenvalues, list), "'eigenvalues' must be an array."
    assert len(computed_eigenvalues) == 5, f"Expected exactly 5 eigenvalues, got {len(computed_eigenvalues)}."

    # Check descending order
    for i in range(len(computed_eigenvalues) - 1):
        assert computed_eigenvalues[i] >= computed_eigenvalues[i+1], "Eigenvalues are not sorted in descending order."

    # Check accuracy against reference
    ref_path = "/home/user/reference_eigenvalues.txt"
    if not os.path.exists(ref_path):
        pytest.fail(f"Reference file {ref_path} is missing.")

    with open(ref_path, "r") as f:
        ref_content = f.read().strip()

    ref_values = [float(x) for x in ref_content.split()]
    assert len(ref_values) == 5, "Reference file should contain exactly 5 values."

    for i, (comp, ref) in enumerate(zip(computed_eigenvalues, ref_values)):
        diff = abs(comp - ref)
        assert diff <= 1e-4, f"Eigenvalue at index {i} ({comp}) differs from reference ({ref}) by {diff}, which is greater than 1e-4."