# test_final_state.py
import os
import json
import subprocess
import pytest

SCRIPT_PATH = '/home/user/query_optimizer.py'
OUTPUT_PATH = '/home/user/optimized_results.json'

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_script_execution_and_output():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

    # Remove output file if it exists to ensure we are testing the current script's output
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    # Run the script with the specified arguments
    result = subprocess.run(
        ['python3', SCRIPT_PATH, 'Python', '5', '0'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed with return code {result.returncode}.\nStderr: {result.stderr}"

    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created after running the script."

    with open(OUTPUT_PATH, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {OUTPUT_PATH} does not contain valid JSON.")

    expected_data = [
        {
            "user_a": "Alice Smith",
            "user_b": "Bob Jones",
            "shared_projects_count": 2
        },
        {
            "user_a": "Alice Smith",
            "user_b": "Charlie Brown",
            "shared_projects_count": 2
        },
        {
            "user_a": "Alice Smith",
            "user_b": "Diana Prince",
            "shared_projects_count": 1
        },
        {
            "user_a": "Charlie Brown",
            "user_b": "Diana Prince",
            "shared_projects_count": 1
        }
    ]

    assert isinstance(data, list), "Output JSON must be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} results, but got {len(data)}."

    for i, (actual, expected) in enumerate(zip(data, expected_data)):
        assert actual == expected, f"Result at index {i} does not match expected.\nExpected: {expected}\nGot: {actual}"

def test_pagination_and_parameterization():
    """Test with different parameters to ensure the script uses arguments correctly."""
    test_output_path = OUTPUT_PATH
    if os.path.exists(test_output_path):
        os.remove(test_output_path)

    # Test with offset 1 and limit 2
    result = subprocess.run(
        ['python3', SCRIPT_PATH, 'Python', '2', '1'],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed for pagination test. Stderr: {result.stderr}"
    assert os.path.isfile(test_output_path), "Output file was not created during pagination test."

    with open(test_output_path, 'r') as f:
        data = json.load(f)

    expected_data = [
        {
            "user_a": "Alice Smith",
            "user_b": "Charlie Brown",
            "shared_projects_count": 2
        },
        {
            "user_a": "Alice Smith",
            "user_b": "Diana Prince",
            "shared_projects_count": 1
        }
    ]

    assert data == expected_data, f"Pagination failed. Expected {expected_data}, Got {data}"