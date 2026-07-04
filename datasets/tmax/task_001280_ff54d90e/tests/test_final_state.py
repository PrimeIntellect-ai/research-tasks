# test_final_state.py

import os
import json
import subprocess
import pytest

def test_output_json_types():
    output_path = "/home/user/output.json"
    assert os.path.isfile(output_path), f"File {output_path} is missing."

    with open(output_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} is not valid JSON.")

    assert isinstance(data, list), "Output JSON should be a list of records."

    for i, row in enumerate(data):
        cat_id = row.get('category_id')
        if cat_id is not None:
            assert isinstance(cat_id, int) and not isinstance(cat_id, float), \
                f"Row {i}: category_id should be int or null, got {type(cat_id).__name__} ({cat_id})"

        tok_len = row.get('token_length')
        if tok_len is not None:
            assert isinstance(tok_len, int) and not isinstance(tok_len, float), \
                f"Row {i}: token_length should be int or null, got {type(tok_len).__name__} ({tok_len})"

def test_pipeline_test_script_exists_and_runs():
    test_script_path = "/home/user/test_pipeline.py"
    assert os.path.isfile(test_script_path), f"File {test_script_path} is missing."

    result = subprocess.run(["python3", test_script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{test_script_path} failed to run. Stderr: {result.stderr}"

def test_benchmark_script_and_output():
    benchmark_script = "/home/user/benchmark.py"
    benchmark_txt = "/home/user/benchmark.txt"

    assert os.path.isfile(benchmark_script), f"File {benchmark_script} is missing."

    # Run the benchmark script if txt doesn't exist, though the user should have run it.
    # We will just check if benchmark.txt exists and contains a float.
    if not os.path.isfile(benchmark_txt):
        # Try running it
        subprocess.run(["python3", benchmark_script], capture_output=True, text=True)

    assert os.path.isfile(benchmark_txt), f"File {benchmark_txt} is missing. Did the benchmark script produce it?"

    with open(benchmark_txt, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {benchmark_txt} is not a valid float string: '{content}'")