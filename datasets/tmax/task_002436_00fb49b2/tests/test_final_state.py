# test_final_state.py

import os
import subprocess
import json
import pytest

@pytest.fixture(scope="session", autouse=True)
def run_analyze():
    """Run the compiled C++ program before running the tests."""
    executable = "/home/user/analyze"
    assert os.path.isfile(executable), f"Executable {executable} not found. Ensure you compiled your C++ code to this path."

    try:
        subprocess.run([executable], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {executable} failed with return code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

def test_final_report_content():
    """Check that the final report contains the correct aggregated averages."""
    report_path = "/home/user/final_report.json"
    assert os.path.isfile(report_path), f"The final report {report_path} was not created."

    with open(report_path, "r") as f:
        content = f.read()

    # The output format might vary slightly depending on how mongosh formatted it,
    # but the location names and their corresponding averages must be present.
    # North: 20.0, South: 22.0, East: 26.0
    assert "North" in content, "Location 'North' is missing from the final report."
    assert "20" in content, "Expected average temperature '20.0' for North is missing."

    assert "South" in content, "Location 'South' is missing from the final report."
    assert "22" in content, "Expected average temperature '22.0' for South is missing."

    assert "East" in content, "Location 'East' is missing from the final report."
    assert "26" in content, "Expected average temperature '26.0' for East is missing."

def test_query_plan_exists():
    """Check that the query plan was saved and contains explain output."""
    plan_path = "/home/user/query_plan.json"
    assert os.path.isfile(plan_path), f"The query plan {plan_path} was not created."

    with open(plan_path, "r") as f:
        content = f.read()

    assert "explainVersion" in content or "executionStats" in content or "queryPlanner" in content, \
        f"The file {plan_path} does not appear to contain MongoDB explain() output."

def test_mongodb_index_created():
    """Check that an appropriate index was created in the iot.readings collection."""
    try:
        result = subprocess.run(
            ["mongosh", "iot", "--quiet", "--eval", "JSON.stringify(db.readings.getIndexes())"],
            capture_output=True,
            text=True,
            check=True
        )
        indexes = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to query MongoDB for indexes. Error: {e.stderr}")
    except json.JSONDecodeError:
        pytest.fail("Failed to parse the index list from MongoDB.")

    # Looking for an index on status, timestamp, or sensor_id
    custom_index_found = False
    for idx in indexes:
        keys = idx.get("key", {})
        if "status" in keys or "timestamp" in keys or "sensor_id" in keys:
            custom_index_found = True
            break

    assert custom_index_found, "No appropriate index (on 'status', 'timestamp', or 'sensor_id') was found in the 'iot.readings' collection."