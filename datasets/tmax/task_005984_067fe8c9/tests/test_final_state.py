# test_final_state.py
import os
import re
import pytest

def test_executable_exists():
    executable_path = "/home/user/etl_project/etl"
    assert os.path.isfile(executable_path), f"Compiled executable not found at {executable_path}"
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable"

def test_tune_script_exists():
    script_path = "/home/user/etl_project/tune.sh"
    assert os.path.isfile(script_path), f"Tuning script not found at {script_path}"

def test_experiment_log_correctness():
    log_path = "/home/user/etl_project/experiment.log"
    csv_path = "/home/user/etl_project/interactions.csv"

    assert os.path.isfile(log_path), f"Experiment log not found at {log_path}"
    assert os.path.isfile(csv_path), f"Data file not found at {csv_path}"

    # Recompute expected values from the actual CSV
    with open(csv_path, "r") as f:
        lines = f.read().strip().splitlines()

    assert len(lines) > 1, "CSV file is empty or missing data rows"

    global_sum = 0.0
    global_count = 0

    user_known_sum = {}
    user_known_count = {}
    missing_entries = []

    for line in lines[1:]:
        parts = line.strip().split(',')
        if len(parts) != 3:
            continue
        u, i, r = parts
        u = int(u)
        if u not in user_known_sum:
            user_known_sum[u] = 0.0
            user_known_count[u] = 0

        if r == '?':
            missing_entries.append(u)
        else:
            rating = float(r)
            global_sum += rating
            global_count += 1
            user_known_sum[u] += rating
            user_known_count[u] += 1

    assert global_count > 0, "No known ratings found in CSV"
    global_avg = global_sum / global_count

    alphas = [1.0, 2.0, 5.0, 10.0]
    expected_outputs = {}

    for alpha in alphas:
        imputed_sum = 0.0
        for u in missing_entries:
            u_sum = user_known_sum.get(u, 0.0)
            u_count = user_known_count.get(u, 0)
            imputed_rating = (u_sum + alpha * global_avg) / (u_count + alpha)
            imputed_sum += imputed_rating
        expected_outputs[alpha] = f"{imputed_sum:.2f}"

    with open(log_path, "r") as f:
        log_content = f.read().strip()

    for alpha in alphas:
        expected_str = f"Alpha: {alpha}, Total Imputed Sum: {expected_outputs[alpha]}"
        # Allow flexible formatting like 1.0 vs 1
        alpha_pattern = f"Alpha:\\s*{alpha}0*\\s*,\\s*Total Imputed Sum:\\s*{expected_outputs[alpha]}"
        assert re.search(alpha_pattern, log_content), f"Expected to find '{expected_str}' in {log_path}, but it was missing or incorrect.\nLog contents:\n{log_content}"