# test_final_state.py
import os
import csv

def test_script_exists_and_executable():
    script_path = "/home/user/process_artifacts.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_posterior_metrics_output():
    log_path = "/home/user/raw_experiments.log"
    csv_path = "/home/user/posterior_metrics.csv"

    assert os.path.isfile(log_path), f"Raw log {log_path} is missing."
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    # Compute expected results from raw log
    models = {}
    with open(log_path, "r") as f:
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            exec_time = row["exec_time_sec"].strip()
            if not exec_time:
                continue
            exec_time = float(exec_time)
            if exec_time < 0 or exec_time > 3600:
                continue

            successes_str = row["successes"].strip()
            if not successes_str:
                continue
            successes = int(successes_str)

            trials_str = row["trials"].strip()
            if not trials_str:
                trials = 1000
            else:
                trials = int(trials_str)

            if successes > trials:
                continue

            model_name = row["model_name"].strip()
            if model_name not in models:
                models[model_name] = {"successes": 0, "failures": 0}

            models[model_name]["successes"] += successes
            models[model_name]["failures"] += (trials - successes)

    expected_rows = []
    for model_name in sorted(models.keys()):
        alpha_post = 1 + models[model_name]["successes"]
        beta_post = 1 + models[model_name]["failures"]
        expected_value = alpha_post / (alpha_post + beta_post)
        expected_rows.append({
            "model_name": model_name,
            "alpha": str(alpha_post),
            "beta": str(beta_post),
            "expected_value": f"{expected_value:.4f}"
        })

    # Read actual results
    actual_rows = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["model_name", "alpha", "beta", "expected_value"], \
            f"CSV header is incorrect. Expected ['model_name', 'alpha', 'beta', 'expected_value'], got {reader.fieldnames}"
        for row in reader:
            actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), \
        f"Expected {len(expected_rows)} rows in CSV, got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual["model_name"] == expected["model_name"], \
            f"Row {i+1}: expected model_name {expected['model_name']}, got {actual['model_name']}"
        assert actual["alpha"] == expected["alpha"], \
            f"Row {i+1} ({actual['model_name']}): expected alpha {expected['alpha']}, got {actual['alpha']}"
        assert actual["beta"] == expected["beta"], \
            f"Row {i+1} ({actual['model_name']}): expected beta {expected['beta']}, got {actual['beta']}"
        assert actual["expected_value"] == expected["expected_value"], \
            f"Row {i+1} ({actual['model_name']}): expected expected_value {expected['expected_value']}, got {actual['expected_value']}"