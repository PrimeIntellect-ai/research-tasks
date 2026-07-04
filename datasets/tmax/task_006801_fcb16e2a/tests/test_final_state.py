# test_final_state.py
import os
import json
import math
import glob
import pytest

def get_valid_runs():
    valid_runs = []
    for filepath in glob.glob('/home/user/experiments/*.json'):
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except Exception:
                continue

            if not isinstance(data, dict):
                continue

            expected_keys = {"run_id", "learning_rate", "batch_size", "num_layers", "metrics"}
            if set(data.keys()) != expected_keys:
                continue

            if not isinstance(data["run_id"], str):
                continue
            if not isinstance(data["learning_rate"], float) and not (isinstance(data["learning_rate"], int) and not isinstance(data["learning_rate"], bool)):
                continue
            if not isinstance(data["batch_size"], int) or isinstance(data["batch_size"], bool):
                continue
            if not isinstance(data["num_layers"], int) or isinstance(data["num_layers"], bool):
                continue

            metrics = data["metrics"]
            if not isinstance(metrics, dict) or set(metrics.keys()) != {"val_accuracy"}:
                continue
            if not isinstance(metrics["val_accuracy"], float) and not (isinstance(metrics["val_accuracy"], int) and not isinstance(metrics["val_accuracy"], bool)):
                continue

            valid_runs.append(data)
    return valid_runs

def compute_expected_closest_runs(valid_runs):
    if not valid_runs:
        return []

    min_lr = min(r["learning_rate"] for r in valid_runs)
    max_lr = max(r["learning_rate"] for r in valid_runs)
    min_bs = min(r["batch_size"] for r in valid_runs)
    max_bs = max(r["batch_size"] for r in valid_runs)
    min_nl = min(r["num_layers"] for r in valid_runs)
    max_nl = max(r["num_layers"] for r in valid_runs)

    def scale(val, min_val, max_val):
        if max_val == min_val:
            return 0.0
        return (val - min_val) / (max_val - min_val)

    target = {"learning_rate": 0.005, "batch_size": 64, "num_layers": 3}
    t_lr = scale(target["learning_rate"], min_lr, max_lr)
    t_bs = scale(target["batch_size"], min_bs, max_bs)
    t_nl = scale(target["num_layers"], min_nl, max_nl)

    distances = []
    for r in valid_runs:
        s_lr = scale(r["learning_rate"], min_lr, max_lr)
        s_bs = scale(r["batch_size"], min_bs, max_bs)
        s_nl = scale(r["num_layers"], min_nl, max_nl)

        dist = math.sqrt((s_lr - t_lr)**2 + (s_bs - t_bs)**2 + (s_nl - t_nl)**2)
        distances.append((dist, r["run_id"]))

    distances.sort(key=lambda x: x[0])
    return [x[1] for x in distances[:3]]

def compute_expected_best_hyperparams(valid_runs):
    groups = {}
    for r in valid_runs:
        key = (r["batch_size"], r["num_layers"])
        groups.setdefault(key, []).append(r["metrics"]["val_accuracy"])

    best_pair = None
    best_mean = -1.0

    for (bs, nl), accuracies in groups.items():
        mean_acc = sum(accuracies) / len(accuracies)
        if mean_acc > best_mean:
            best_mean = mean_acc
            best_pair = (bs, nl)
        elif mean_acc == best_mean:
            if best_pair is None or bs > best_pair[0]:
                best_pair = (bs, nl)

    if best_pair is None:
        return ""

    return f"{best_pair[0]},{best_pair[1]},{best_mean:.4f}"

def test_closest_runs():
    output_path = '/home/user/closest_runs.json'
    assert os.path.exists(output_path), f"File {output_path} does not exist."

    with open(output_path, 'r') as f:
        try:
            student_closest = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{output_path} is not valid JSON.")

    valid_runs = get_valid_runs()
    expected_closest = compute_expected_closest_runs(valid_runs)

    assert student_closest == expected_closest, f"Expected closest runs {expected_closest}, but got {student_closest}"

def test_best_hyperparams():
    output_path = '/home/user/best_hyperparams.txt'
    assert os.path.exists(output_path), f"File {output_path} does not exist."

    with open(output_path, 'r') as f:
        student_best = f.read().strip()

    valid_runs = get_valid_runs()
    expected_best = compute_expected_best_hyperparams(valid_runs)

    assert student_best == expected_best, f"Expected best hyperparams '{expected_best}', but got '{student_best}'"