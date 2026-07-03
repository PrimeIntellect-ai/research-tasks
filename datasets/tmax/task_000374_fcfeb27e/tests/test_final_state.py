# test_final_state.py
import os
import csv

def test_script_exists_and_executable():
    script_path = "/home/user/prepare_data.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_dataset_output():
    dataset_path = "/home/user/dataset_run_baseline.csv"
    assert os.path.isfile(dataset_path), f"Dataset file {dataset_path} does not exist."

    expected_data = [
        ["method", "status", "url_len", "param_count", "suspicious", "tokenized_url"],
        ["GET", "200", "11", "0", "0", "index html"],
        ["POST", "401", "30", "2", "0", "login php user admin pass 123"],
        ["GET", "403", "35", "1", "1", "search q script alert 1 script"],
        ["GET", "200", "39", "2", "1", "api data id 1 token base64 encoded str"],
        ["PUT", "201", "16", "0", "0", "upload test txt"]
    ]

    with open(dataset_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert actual_data == expected_data, f"Content of {dataset_path} does not match expected output. Got: {actual_data}"

def test_experiment_log_output():
    log_path = "/home/user/experiment_log.csv"
    assert os.path.isfile(log_path), f"Experiment log file {log_path} does not exist."

    expected_data = [
        ["experiment_id", "total_rows", "suspicious_count"],
        ["run_baseline", "5", "2"]
    ]

    with open(log_path, "r", newline="") as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert actual_data == expected_data, f"Content of {log_path} does not match expected output. Got: {actual_data}"