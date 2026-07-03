# test_final_state.py

import os
import subprocess
import pytest

def test_fast_query_exists_and_optimized():
    path = "/home/user/fast_query.rq"
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "?m2" not in content, "Query was not properly optimized (still contains multiple movie variables like ?m2)."

def test_export_results_script_exists_and_executable():
    path = "/home/user/export_results.sh"
    assert os.path.isfile(path), f"File missing: {path}"
    assert os.access(path, os.X_OK), f"Script is not executable: {path}"

def test_export_results_output():
    script_path = "/home/user/export_results.sh"
    results_path = "/home/user/results.csv"

    # Remove results.csv if it exists to ensure the script creates it
    if os.path.exists(results_path):
        os.remove(results_path)

    # Run the script
    result = subprocess.run(
        [script_path],
        cwd="/home/user",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"export_results.sh failed with return code {result.returncode}\nStderr: {result.stderr}"

    assert os.path.isfile(results_path), f"Script did not create {results_path}"

    with open(results_path, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "Actor",
        "Bill Paxton",
        "Finn Carter",
        "Fred Ward",
        "John Lithgow",
        "Lori Singer",
        "Tom Hanks"
    ]

    assert content == expected, f"Contents of {results_path} do not match the expected output. Got: {content}"