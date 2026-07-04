# test_final_state.py

import os
import json
import subprocess
import pytest

def test_result_json():
    result_path = "/home/user/result.json"
    assert os.path.isfile(result_path), f"Missing {result_path}"

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{result_path} is not a valid JSON file")

    assert data.get("secret_node_id") == "NODE_ID_8192", "Incorrect secret_node_id in result.json"
    assert data.get("filter_script_path") == "/home/user/query_filter.py", "Incorrect filter_script_path in result.json"

def test_query_filter_script_exists():
    script_path = "/home/user/query_filter.py"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

def test_query_filter_clean_corpus():
    script_path = "/home/user/query_filter.py"
    clean_dir = "/app/corpus/clean/"

    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"
    expected_files = {f for f in os.listdir(clean_dir) if f.endswith(".cypher")}

    result = subprocess.run(
        ["python3", script_path, clean_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed on clean corpus with error: {result.stderr}"

    output_lines = set(line.strip() for line in result.stdout.strip().split("\n") if line.strip())

    missing_files = expected_files - output_lines
    extra_files = output_lines - expected_files

    assert not missing_files, f"{len(missing_files)} of {len(expected_files)} clean files were rejected. Missing: {missing_files}"
    assert not extra_files, f"Script output extra unexpected filenames for clean corpus: {extra_files}"

def test_query_filter_evil_corpus():
    script_path = "/home/user/query_filter.py"
    evil_dir = "/app/corpus/evil/"

    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"
    evil_files = {f for f in os.listdir(evil_dir) if f.endswith(".cypher")}

    result = subprocess.run(
        ["python3", script_path, evil_dir],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed on evil corpus with error: {result.stderr}"

    output_lines = set(line.strip() for line in result.stdout.strip().split("\n") if line.strip())

    bypassed_files = output_lines.intersection(evil_files)
    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed the filter. Bypassed: {bypassed_files}"