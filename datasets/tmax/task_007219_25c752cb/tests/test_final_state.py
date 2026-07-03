# test_final_state.py

import os
import csv
import pytest

def compute_expected_results():
    source_a_path = "/home/user/source_a.csv"
    source_b_path = "/home/user/source_b.csv"

    assert os.path.exists(source_a_path), f"{source_a_path} is missing."
    assert os.path.exists(source_b_path), f"{source_b_path} is missing."

    data = {}
    with open(source_a_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exp_id = int(row["ExperimentID"])
            data[exp_id] = {
                "M1": float(row["Metric1"]),
                "M2": float(row["Metric2"])
            }

    with open(source_b_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            exp_id = int(row["ExperimentID"])
            if exp_id in data:
                data[exp_id]["M3"] = float(row["Metric3"])
                data[exp_id]["Prior"] = float(row["PriorProb"])

    # Impute missing values (-999.0)
    for metric in ["M1", "M2", "M3"]:
        valid_values = [d[metric] for d in data.values() if d[metric] != -999.0]
        mean_val = sum(valid_values) / len(valid_values) if valid_values else 0.0
        for exp_id in data:
            if data[exp_id][metric] == -999.0:
                data[exp_id][metric] = mean_val

    # Calculate population variance
    total_variance = 0.0
    for metric in ["M1", "M2", "M3"]:
        values = [d[metric] for d in data.values()]
        mean_val = sum(values) / len(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        total_variance += variance

    # Calculate Bayesian Posterior
    max_posterior = -1.0
    best_exp_id = -1

    for exp_id, d in data.items():
        metric_sum = d["M1"] + d["M2"] + d["M3"]
        prior = d["Prior"]

        if metric_sum > 20.0:
            l_success = 0.8
            l_fail = 0.3
        else:
            l_success = 0.4
            l_fail = 0.7

        marginal = (l_success * prior) + (l_fail * (1.0 - prior))
        posterior = (l_success * prior) / marginal

        if posterior > max_posterior:
            max_posterior = posterior
            best_exp_id = exp_id

    return best_exp_id, total_variance

def test_summary_file_exists():
    assert os.path.exists("/home/user/summary.txt"), "The summary.txt file was not found."

def test_cpp_file_exists():
    assert os.path.exists("/home/user/tracker.cpp"), "The tracker.cpp file was not found."

def test_summary_content():
    expected_exp_id, expected_total_variance = compute_expected_results()

    with open("/home/user/summary.txt", "r") as f:
        content = f.read().strip()

    lines = content.split('\n')
    assert len(lines) >= 2, "summary.txt does not contain enough lines."

    exp_id_line = lines[0].strip()
    variance_line = lines[1].strip()

    assert exp_id_line.startswith("Highest_Posterior_Exp_ID:"), "First line format is incorrect."
    assert variance_line.startswith("Total_Variance:"), "Second line format is incorrect."

    actual_exp_id = int(exp_id_line.split(":")[1].strip())
    actual_variance = float(variance_line.split(":")[1].strip())

    assert actual_exp_id == expected_exp_id, f"Expected Highest_Posterior_Exp_ID to be {expected_exp_id}, but got {actual_exp_id}."

    expected_variance_str = f"{expected_total_variance:.2f}"
    actual_variance_str = f"{actual_variance:.2f}"

    assert actual_variance_str == expected_variance_str, f"Expected Total_Variance to be {expected_variance_str}, but got {actual_variance_str}."