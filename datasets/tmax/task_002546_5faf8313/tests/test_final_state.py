# test_final_state.py
import os
import json
import csv
import math
import subprocess
import pytest

def get_vec(text):
    t = text.lower()
    bigrams = ["th", "he", "in", "er", "an"]
    vec = []
    for bg in bigrams:
        count = 0
        for i in range(len(t)-1):
            if t[i:i+2] == bg:
                count += 1
        vec.append(count)
    return vec

def dist(v1, v2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

def compute_expected():
    data_path = "/home/user/data.csv"
    dataset = []
    with open(data_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            dataset.append((get_vec(row["text"]), row["label"]))

    accuracies = {}
    for k in [1, 2, 3]:
        correct = 0
        for i in range(len(dataset)):
            test_vec, test_label = dataset[i]

            dists = []
            for j in range(len(dataset)):
                if i == j: continue
                train_vec, train_label = dataset[j]
                dists.append((dist(test_vec, train_vec), train_label))

            dists.sort(key=lambda x: x[0])
            neighbors = dists[:k]

            counts = {}
            for d, l in neighbors:
                counts[l] = counts.get(l, 0) + 1

            # tie break alphabetically
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            pred = sorted_counts[0][0]

            if pred == test_label:
                correct += 1

        accuracies[k] = correct / len(dataset)

    best_k = 1
    best_acc = -1
    for k in [1, 2, 3]:
        if accuracies[k] > best_acc:
            best_acc = accuracies[k]
            best_k = k

    return best_k, best_acc

def test_rust_project_setup():
    project_dir = "/home/user/dataset_organizer"
    assert os.path.isdir(project_dir), f"Rust project directory missing at {project_dir}"
    cargo_toml = os.path.join(project_dir, "Cargo.toml")
    assert os.path.isfile(cargo_toml), f"Cargo.toml missing at {cargo_toml}"
    main_rs = os.path.join(project_dir, "src", "main.rs")
    assert os.path.isfile(main_rs), f"src/main.rs missing at {main_rs}"

def test_run_pipeline_script():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

    # Run the pipeline script to ensure reproducibility
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with return code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_best_model_output():
    json_path = "/home/user/best_model.json"
    assert os.path.isfile(json_path), f"Output JSON file missing at {json_path}"

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} does not contain valid JSON.")

    assert "best_k" in data, f"'best_k' missing in {json_path}"
    assert "accuracy" in data, f"'accuracy' missing in {json_path}"

    expected_k, expected_acc = compute_expected()

    assert data["best_k"] == expected_k, f"Expected best_k to be {expected_k}, got {data['best_k']}"
    assert abs(data["accuracy"] - expected_acc) < 1e-5, f"Expected accuracy to be {expected_acc}, got {data['accuracy']}"