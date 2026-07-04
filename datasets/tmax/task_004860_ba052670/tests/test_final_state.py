# test_final_state.py

import os
import json
import subprocess
import pytest

def test_reaction_params():
    params_path = "/home/user/reaction_params.json"
    assert os.path.exists(params_path), f"Missing {params_path}"

    with open(params_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {params_path} is not valid JSON.")

    required_keys = [
        "k_mean", "k_ci_lower", "k_ci_upper",
        "c_mean", "c_ci_lower", "c_ci_upper"
    ]
    for key in required_keys:
        assert key in data, f"Missing key {key} in {params_path}"

    k_mean = data["k_mean"]
    c_mean = data["c_mean"]

    assert 0.42 <= k_mean <= 0.48, f"k_mean {k_mean} out of bounds [0.42, 0.48]"
    assert 0.12 <= c_mean <= 0.18, f"c_mean {c_mean} out of bounds [0.12, 0.18]"

    assert data["k_ci_lower"] < k_mean < data["k_ci_upper"], "k_ci values are not mathematically sensible (lower < mean < upper)"
    assert data["c_ci_lower"] < c_mean < data["c_ci_upper"], "c_ci values are not mathematically sensible (lower < mean < upper)"

def test_stability_filter_executable():
    exe_path = "/home/user/stability_filter"
    assert os.path.exists(exe_path), f"Missing executable {exe_path}"
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable"

def test_stability_filter_clean_corpus():
    exe_path = "/home/user/stability_filter"
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Missing clean corpus directory: {clean_dir}"

    failed_files = []
    total = 0
    for fname in sorted(os.listdir(clean_dir)):
        fpath = os.path.join(clean_dir, fname)
        if os.path.isfile(fpath):
            total += 1
            res = subprocess.run([exe_path, fpath], capture_output=True)
            if res.returncode != 0:
                failed_files.append(fname)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total} clean modified (rejected when they should be accepted): {', '.join(failed_files)}")

def test_stability_filter_evil_corpus():
    exe_path = "/home/user/stability_filter"
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Missing evil corpus directory: {evil_dir}"

    failed_files = []
    total = 0
    for fname in sorted(os.listdir(evil_dir)):
        fpath = os.path.join(evil_dir, fname)
        if os.path.isfile(fpath):
            total += 1
            res = subprocess.run([exe_path, fpath], capture_output=True)
            if res.returncode != 1:
                failed_files.append(fname)

    if failed_files:
        pytest.fail(f"{len(failed_files)} of {total} evil bypassed (accepted when they should be rejected): {', '.join(failed_files)}")