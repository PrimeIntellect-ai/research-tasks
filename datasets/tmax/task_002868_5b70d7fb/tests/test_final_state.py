# test_final_state.py
import os
import math
import json
import hashlib

def get_embed(s):
    vec = [0.0] * 16
    for i in range(16):
        acc = sum(ord(c) * (i + 1) for c in s.strip('\n'))
        vec[i] = acc % 100
    norm = math.sqrt(sum(v*v for v in vec))
    if norm > 0:
        vec = [v/norm for v in vec]
    return vec

def dot(v1, v2):
    return sum(x*y for x, y in zip(v1, v2))

def compute_expected_cleaned_data():
    raw_path = "/home/user/data/raw_dataset.txt"
    if not os.path.exists(raw_path):
        return []

    with open(raw_path, "r") as f:
        lines = f.readlines()

    accepted = []
    kept_lines = []

    for line in lines:
        emb = get_embed(line)
        is_dup = False
        for a_emb in accepted:
            if dot(emb, a_emb) >= 0.90:
                is_dup = True
                break
        if not is_dup:
            accepted.append(emb)
            kept_lines.append(line)

    return kept_lines

def test_files_exist():
    expected_files = [
        "/home/user/cleaner.cpp",
        "/home/user/Makefile",
        "/home/user/run_pipeline.sh",
        "/home/user/data/cleaned_dataset.txt",
        "/home/user/data/benchmark.json",
        "/home/user/data/reproducibility_hash.txt"
    ]
    for f in expected_files:
        assert os.path.isfile(f), f"Expected file {f} is missing."

def test_run_pipeline_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_cleaned_dataset_content():
    expected_lines = compute_expected_cleaned_data()
    path = "/home/user/data/cleaned_dataset.txt"
    with open(path, "r") as f:
        actual_lines = f.readlines()

    assert actual_lines == expected_lines, "The contents of cleaned_dataset.txt do not match the expected output based on the embedding and filtering logic."

def test_benchmark_json():
    expected_lines = compute_expected_cleaned_data()
    path = "/home/user/data/benchmark.json"
    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "benchmark.json is not a valid JSON file."

    expected_keys = {"total_lines", "kept_lines", "time_seconds", "throughput_lines_per_sec"}
    assert expected_keys.issubset(data.keys()), f"benchmark.json is missing one or more required keys: {expected_keys - data.keys()}"

    assert data["total_lines"] == 500, f"Expected total_lines to be 500, got {data['total_lines']}"
    assert data["kept_lines"] == len(expected_lines), f"Expected kept_lines to be {len(expected_lines)}, got {data['kept_lines']}"
    assert isinstance(data["time_seconds"], (int, float)), "time_seconds must be a number."
    assert isinstance(data["throughput_lines_per_sec"], (int, float)), "throughput_lines_per_sec must be a number."

def test_reproducibility_hash():
    cleaned_path = "/home/user/data/cleaned_dataset.txt"
    hash_path = "/home/user/data/reproducibility_hash.txt"

    with open(cleaned_path, "rb") as f:
        expected_hash = hashlib.sha256(f.read()).hexdigest()

    with open(hash_path, "r") as f:
        actual_hash = f.read().strip().split()[0]

    assert actual_hash == expected_hash, f"The hash in reproducibility_hash.txt ({actual_hash}) does not match the actual SHA-256 hash of cleaned_dataset.txt ({expected_hash})."