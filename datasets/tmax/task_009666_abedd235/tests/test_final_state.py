# test_final_state.py

import os
import json
import shutil
import subprocess
import pytest

def test_roqet_installed():
    """Check if rasqal-utils (roqet) is installed."""
    assert shutil.which("roqet") is not None, "The 'roqet' command is not installed. Did you install 'rasqal-utils'?"

def test_optimized_query_script():
    """Check if optimized_query.sh exists and is executable."""
    script_path = "/home/user/optimized_query.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_results_json():
    """Check if results.json contains the correct SPARQL JSON output."""
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

    try:
        with open(results_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {results_path} does not contain valid JSON.")

    assert "results" in data and "bindings" in data["results"], "JSON does not match SPARQL Query Results JSON Format."

    bindings = data["results"]["bindings"]
    assert len(bindings) == 2, f"Expected exactly 2 results due to LIMIT 2, but got {len(bindings)}."

    # Expected results sorted alphabetically: Alice, then Charlie
    expected_names = ["Alice", "Charlie"]

    for i, expected_name in enumerate(expected_names):
        binding = bindings[i]
        assert "employeeName" in binding, f"Result {i+1} is missing the 'employeeName' variable."
        assert "server" in binding, f"Result {i+1} is missing the 'server' variable."

        actual_name = binding["employeeName"]["value"]
        assert actual_name == expected_name, f"Expected employeeName '{expected_name}' at position {i+1}, but got '{actual_name}'."

        # Check server matches expectation
        actual_server = binding["server"]["value"]
        if expected_name == "Alice":
            assert "Server1" in actual_server, f"Alice should be associated with Server1, got {actual_server}"
        elif expected_name == "Charlie":
            assert "Server3" in actual_server, f"Charlie should be associated with Server3, got {actual_server}"

def test_script_dynamic_parameter():
    """Test if optimized_query.sh dynamically accepts the vulnerability ID parameter."""
    script_path = "/home/user/optimized_query.sh"

    # Run the script with the other vulnerability
    result = subprocess.run(
        [script_path, "CVE-2023-9999"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Running {script_path} failed with error:\n{result.stderr}"

    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Output of {script_path} is not valid JSON. Make sure it prints the roqet output to stdout.")

    bindings = data.get("results", {}).get("bindings", [])

    # CVE-2023-9999 is SoftwareB, which runs on Server2. Only Bob accesses Server2.
    assert len(bindings) == 1, f"Expected exactly 1 result for CVE-2023-9999, but got {len(bindings)}."
    assert bindings[0]["employeeName"]["value"] == "Bob", "Expected employeeName 'Bob' for CVE-2023-9999."
    assert "Server2" in bindings[0]["server"]["value"], "Expected Server2 for CVE-2023-9999."