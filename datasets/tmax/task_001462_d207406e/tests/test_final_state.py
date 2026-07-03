# test_final_state.py

import os
import csv
import subprocess
import ast

def test_files_exist():
    """Verify that all required scripts and output files exist."""
    assert os.path.isfile("/home/user/pipeline.py"), "/home/user/pipeline.py is missing."
    assert os.path.isfile("/home/user/test_pipeline.py"), "/home/user/test_pipeline.py is missing."
    assert os.path.isdir("/home/user/output"), "/home/user/output directory is missing."
    assert os.path.isfile("/home/user/output/results.csv"), "/home/user/output/results.csv is missing."
    assert os.path.isfile("/home/user/output/top_spectrum.png"), "/home/user/output/top_spectrum.png is missing."

def test_results_csv_content():
    """Verify the content of results.csv."""
    csv_path = "/home/user/output/results.csv"
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, "results.csv is empty."

    header = rows[0]
    expected_header = ["SequenceID", "MaxPowerIndex", "MaxPowerValue"]
    assert header == expected_header, f"CSV header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]
    assert len(data_rows) == 3, f"Expected 3 data rows in CSV, got {len(data_rows)}."

    # Check sorting by SequenceID
    seq_ids = [row[0] for row in data_rows]
    assert seq_ids == sorted(seq_ids), "CSV rows are not sorted alphabetically by SequenceID."

    # Parse rows into a dictionary for easier checking
    results = {row[0]: {"index": int(row[1]), "value": float(row[2])} for row in data_rows}

    assert "SeqA_periodic" in results, "SeqA_periodic missing from results."
    assert "SeqB_flat" in results, "SeqB_flat missing from results."
    assert "SeqC_random" in results, "SeqC_random missing from results."

    # SeqA_periodic checks
    # Period is 4, sequence length 120, so max power index should be 30 (or 90)
    assert results["SeqA_periodic"]["index"] in [30, 90], f"SeqA_periodic MaxPowerIndex should be 30 or 90, got {results['SeqA_periodic']['index']}."
    assert abs(results["SeqA_periodic"]["value"] - 112.5) < 0.1, f"SeqA_periodic MaxPowerValue should be near 112.5, got {results['SeqA_periodic']['value']}."

    # SeqB_flat checks
    assert abs(results["SeqB_flat"]["value"]) < 0.001, f"SeqB_flat MaxPowerValue should be near 0.0, got {results['SeqB_flat']['value']}."

def test_png_is_valid():
    """Check that top_spectrum.png is a valid PNG file."""
    png_path = "/home/user/output/top_spectrum.png"
    with open(png_path, "rb") as f:
        header = f.read(8)
    assert header == b"\x89PNG\r\n\x1a\n", "top_spectrum.png is not a valid PNG file."

def test_multiprocessing_used():
    """Verify that multiprocessing is imported and used in pipeline.py."""
    with open("/home/user/pipeline.py", "r") as f:
        source = f.read()

    tree = ast.parse(source)

    multiprocessing_imported = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if "multiprocessing" in alias.name:
                    multiprocessing_imported = True
        elif isinstance(node, ast.ImportFrom):
            if node.module and "multiprocessing" in node.module:
                multiprocessing_imported = True

    assert multiprocessing_imported, "The 'multiprocessing' module is not imported in pipeline.py."

def test_pytest_suite_passes():
    """Run the student's pytest suite and ensure it passes."""
    result = subprocess.run(
        ["pytest", "/home/user/test_pipeline.py"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Student's pytest suite failed:\n{result.stdout}\n{result.stderr}"
    assert "passed" in result.stdout.lower() or "1 passed" in result.stdout.lower(), "Pytest output does not indicate passing tests."