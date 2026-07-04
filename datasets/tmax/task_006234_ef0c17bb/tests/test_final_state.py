# test_final_state.py

import os
import json
import stat
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/process_sets.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_jq_downloaded_and_executable():
    jq_path = "/home/user/bin/jq"
    assert os.path.isfile(jq_path), f"jq binary {jq_path} does not exist."
    st = os.stat(jq_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"jq binary {jq_path} is not executable."

def test_sum_calculation():
    set_a_path = "/home/user/data/set_A.json"
    set_b_path = "/home/user/data/set_B.json"
    sum_path = "/home/user/sum.txt"

    # Recompute expected sum
    with open(set_a_path, 'r') as f:
        set_a = set(json.load(f).get("numbers", []))
    with open(set_b_path, 'r') as f:
        set_b = set(json.load(f).get("numbers", []))

    expected_sum = sum(set_a.intersection(set_b))

    assert os.path.isfile(sum_path), f"Output file {sum_path} does not exist."
    with open(sum_path, 'r') as f:
        content = f.read().strip()

    assert content == str(expected_sum), f"Expected sum {expected_sum}, but got {content} in {sum_path}."

def test_benchmark_output():
    benchmark_path = "/home/user/benchmark.txt"
    assert os.path.isfile(benchmark_path), f"Benchmark output {benchmark_path} does not exist."

    with open(benchmark_path, 'r') as f:
        content = f.read()

    assert "real" in content, f"'real' not found in {benchmark_path}"
    assert "user" in content, f"'user' not found in {benchmark_path}"
    assert "sys" in content, f"'sys' not found in {benchmark_path}"