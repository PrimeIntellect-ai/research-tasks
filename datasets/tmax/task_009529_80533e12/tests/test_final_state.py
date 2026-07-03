# test_final_state.py

import os
import json
import math
import subprocess

PIPELINE_DIR = "/home/user/pipeline"
OUTPUT_FILE = os.path.join(PIPELINE_DIR, "final_output.json")
REQUIREMENTS_FILE = os.path.join(PIPELINE_DIR, "requirements.txt")

def test_final_output_exists():
    assert os.path.isfile(OUTPUT_FILE), (
        f"The file {OUTPUT_FILE} was not generated. The pipeline likely failed to run "
        "or the environment variable was not set correctly."
    )

def test_final_output_correctness():
    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{OUTPUT_FILE} is not a valid JSON file."

    # Check concurrency fix
    assert "records_processed" in data, "Key 'records_processed' is missing from the JSON output."
    assert data["records_processed"] == 10000, (
        f"Expected exactly 10000 records processed, but got {data['records_processed']}. "
        "The race condition in processor.py might not be fully fixed."
    )

    # Check precision loss fix
    assert "total_weight" in data, "Key 'total_weight' is missing from the JSON output."

    # Recompute the expected truth value robustly
    weights = [1e16, 1.2345, -1e16, 2.3456]
    expected_weight = math.fsum(weights)
    actual_weight = data["total_weight"]

    assert math.isclose(actual_weight, expected_weight, rel_tol=1e-9), (
        f"Expected total_weight to be exactly {expected_weight}, but got {actual_weight}. "
        "The precision loss in aggregator.py has not been fixed properly."
    )

def test_requirements_installable():
    assert os.path.isfile(REQUIREMENTS_FILE), f"{REQUIREMENTS_FILE} is missing."

    # Use pip's --dry-run to verify that the requirements can be resolved and installed without conflicts
    result = subprocess.run(
        ["python3", "-m", "pip", "install", "--dry-run", "-r", REQUIREMENTS_FILE],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"The requirements.txt file still contains conflicts or cannot be installed.\n"
        f"Error output:\n{result.stderr}\n{result.stdout}"
    )