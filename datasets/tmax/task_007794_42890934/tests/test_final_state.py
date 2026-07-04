# test_final_state.py

import os
import pytest

def test_go_mod_exists():
    go_mod_path = "/home/user/go.mod"
    assert os.path.exists(go_mod_path), f"The file {go_mod_path} is missing. Did you initialize the Go module?"
    with open(go_mod_path, "r") as f:
        content = f.read()
    assert "module webfeature" in content, f"The file {go_mod_path} does not contain 'module webfeature'."

def test_journey_go_exists():
    journey_go_path = "/home/user/journey.go"
    assert os.path.exists(journey_go_path), f"The file {journey_go_path} is missing."
    assert os.path.isfile(journey_go_path), f"The path {journey_go_path} is not a file."

def test_completed_users_txt():
    completed_users_path = "/home/user/completed_users.txt"
    assert os.path.exists(completed_users_path), f"The file {completed_users_path} is missing."

    expected_users = ["user_b", "user_c", "user_e"]

    with open(completed_users_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == expected_users, f"The content of {completed_users_path} is incorrect. Expected {expected_users}, but got {lines}."

def test_journey_test_go_exists():
    journey_test_go_path = "/home/user/journey_test.go"
    assert os.path.exists(journey_test_go_path), f"The file {journey_test_go_path} is missing. Did you write the benchmark test?"
    assert os.path.isfile(journey_test_go_path), f"The path {journey_test_go_path} is not a file."

def test_bench_txt():
    bench_txt_path = "/home/user/bench.txt"
    assert os.path.exists(bench_txt_path), f"The file {bench_txt_path} is missing. Did you run the benchmark and redirect output?"

    with open(bench_txt_path, "r") as f:
        content = f.read()

    assert "Benchmark" in content, f"The file {bench_txt_path} does not seem to contain standard Go benchmark output."