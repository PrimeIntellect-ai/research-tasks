# test_final_state.py
import os
import json
import xml.etree.ElementTree as ET
import pytest

BASE_DIR = "/home/user/sensor_data"
C_SOURCE = "/home/user/aggregate.c"
C_EXEC = "/home/user/aggregate"
FINAL_XML = "/home/user/final_results.xml"

def test_jsonl_converted_to_csv():
    """Verify that site_beta has CSV files and they are correctly formatted."""
    site_beta = os.path.join(BASE_DIR, "site_beta")
    assert os.path.isdir(site_beta), f"Directory {site_beta} is missing."

    for day in range(1, 4):
        csv_file = os.path.join(site_beta, f"2023-05-{day:02d}.csv")
        assert os.path.isfile(csv_file), f"Converted CSV file {csv_file} is missing."

        with open(csv_file, 'r') as f:
            lines = f.read().strip().split('\n')

        assert len(lines) > 1, f"CSV file {csv_file} is empty or missing data."
        assert lines[0].strip() == "timestamp,temperature,humidity", f"CSV file {csv_file} has incorrect header."

        # Check a data line
        parts = lines[1].split(',')
        assert len(parts) == 3, f"CSV file {csv_file} has incorrect data format."

def test_c_program_exists_and_compiled():
    """Verify the C source and executable exist."""
    assert os.path.isfile(C_SOURCE), f"C source file {C_SOURCE} is missing."
    assert os.path.isfile(C_EXEC), f"Compiled executable {C_EXEC} is missing."
    assert os.access(C_EXEC, os.X_OK), f"File {C_EXEC} is not executable."

def test_final_results_xml():
    """Verify the final XML output matches the expected computed values."""
    assert os.path.isfile(FINAL_XML), f"Final XML file {FINAL_XML} is missing."

    valid_t = []
    # Recompute the expected metrics from the files
    for root, _, files in os.walk(BASE_DIR):
        for file in files:
            # We process both .csv and .jsonl in case the user didn't delete .jsonl
            # But we only want to count each record once. 
            # If a .csv exists, we use it. If not, we use .jsonl.
            if file.endswith(".csv"):
                with open(os.path.join(root, file), 'r') as f:
                    lines = f.readlines()
                    if not lines: continue
                    if "timestamp" in lines[0]:
                        lines = lines[1:]
                    for line in lines:
                        if not line.strip(): continue
                        parts = line.strip().split(',')
                        if len(parts) == 3:
                            try:
                                t = float(parts[1])
                                h = float(parts[2])
                                if -50.0 <= t <= 60.0 and 0.0 <= h <= 100.0:
                                    valid_t.append(t)
                            except ValueError:
                                pass

    assert len(valid_t) > 0, "No valid temperature records found to compute metrics."

    expected_max = max(valid_t)
    expected_min = min(valid_t)
    expected_avg = sum(valid_t) / len(valid_t)

    # Parse the user's XML
    try:
        tree = ET.parse(FINAL_XML)
        root = tree.getroot()
    except ET.ParseError as e:
        pytest.fail(f"Failed to parse {FINAL_XML} as valid XML: {e}")

    assert root.tag == "results", f"Root element of XML should be 'results', got '{root.tag}'."

    metrics = root.find("metrics")
    assert metrics is not None, "Missing 'metrics' element in XML."

    max_temp_elem = metrics.find("max_temp")
    min_temp_elem = metrics.find("min_temp")
    avg_temp_elem = metrics.find("avg_temp")

    assert max_temp_elem is not None, "Missing 'max_temp' element."
    assert min_temp_elem is not None, "Missing 'min_temp' element."
    assert avg_temp_elem is not None, "Missing 'avg_temp' element."

    try:
        actual_max = float(max_temp_elem.text)
        actual_min = float(min_temp_elem.text)
        actual_avg = float(avg_temp_elem.text)
    except (ValueError, TypeError):
        pytest.fail("XML elements do not contain valid float values.")

    assert abs(actual_max - expected_max) < 0.02, f"Expected max_temp ~{expected_max:.2f}, got {actual_max}"
    assert abs(actual_min - expected_min) < 0.02, f"Expected min_temp ~{expected_min:.2f}, got {actual_min}"
    assert abs(actual_avg - expected_avg) < 0.02, f"Expected avg_temp ~{expected_avg:.2f}, got {actual_avg}"