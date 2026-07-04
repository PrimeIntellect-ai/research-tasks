# test_final_state.py

import os
import stat
import py_compile
import pytest

def test_processor_py_exists_and_valid():
    path = "/home/user/processor.py"
    assert os.path.isfile(path), f"Expected {path} to exist."

    try:
        py_compile.compile(path, doraise=True)
    except py_compile.PyCompileError as e:
        pytest.fail(f"{path} is not valid Python 3 code: {e}")

def test_pipeline_sh_exists_and_executable():
    path = "/home/user/pipeline.sh"
    assert os.path.isfile(path), f"Expected {path} to exist."

    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Expected {path} to be executable."

def test_merged_csv_matches_baseline():
    merged_path = "/home/user/merged.csv"
    baseline_path = "/home/user/baseline.csv"

    assert os.path.isfile(merged_path), f"Expected {merged_path} to exist."
    assert os.path.isfile(baseline_path), f"Expected {baseline_path} to exist."

    with open(merged_path, "r", encoding="utf-8") as f:
        merged_content = f.read().strip()

    with open(baseline_path, "r", encoding="utf-8") as f:
        baseline_content = f.read().strip()

    assert merged_content == baseline_content, "The content of merged.csv does not match baseline.csv."

def test_diff_report_empty():
    path = "/home/user/diff_report.txt"
    assert os.path.isfile(path), f"Expected {path} to exist."

    size = os.path.getsize(path)
    assert size == 0, f"Expected {path} to be exactly 0 bytes (empty), but got {size} bytes."

def test_github_actions_workflow_exists_and_valid():
    path = "/home/user/.github/workflows/data_pipeline.yml"
    assert os.path.isfile(path), f"Expected {path} to exist."

    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "push" in content, f"Expected 'push' trigger in {path}."
    assert "3.9" in content, f"Expected python-version 3.9 in {path}."
    assert "diff_report.txt" in content, f"Expected check on diff_report.txt in {path}."
    assert "ubuntu-latest" in content, f"Expected ubuntu-latest runner in {path}."