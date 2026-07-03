# test_final_state.py
import os
import json
import pytest

WORKSPACE_DIR = "/home/user/workspace"
RESULTS_FILE = os.path.join(WORKSPACE_DIR, "results.json")

EXPECTED_MSE = {
    "data1.csv": 0.004,
    "data2.csv": 0.0,
    "data3.csv": 0.004
}

def test_results_json_exists_and_valid():
    assert os.path.isfile(RESULTS_FILE), f"Results file {RESULTS_FILE} is missing. Did you run the script and save the output?"

    with open(RESULTS_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {RESULTS_FILE} is not valid JSON.")

    assert isinstance(data, list), f"Expected {RESULTS_FILE} to contain a JSON array, but got {type(data).__name__}."
    assert len(data) == 3, f"Expected exactly 3 results in {RESULTS_FILE}, found {len(data)}. Did you run the script on all datasets and append correctly?"

def test_results_json_content():
    with open(RESULTS_FILE, "r") as f:
        data = json.load(f)

    datasets_found = []
    for item in data:
        assert "dataset" in item, "Missing 'dataset' key in result object."
        assert "mse" in item, "Missing 'mse' key in result object."
        assert "inference_time_sec" in item, "Missing 'inference_time_sec' key in result object."

        dataset = item["dataset"]
        # Allow path prefixes if the user passed full paths
        dataset_name = os.path.basename(dataset)
        datasets_found.append(dataset_name)

        assert dataset_name in EXPECTED_MSE, f"Unexpected dataset name {dataset_name} found in results."

        expected_mse = EXPECTED_MSE[dataset_name]
        actual_mse = item["mse"]

        assert abs(actual_mse - expected_mse) < 1e-3, f"Incorrect MSE for {dataset_name}. Expected ~{expected_mse}, got {actual_mse}. Did you fix the MSE calculation?"

        inference_time = item["inference_time_sec"]
        assert inference_time < 0.1, f"Inference time for {dataset_name} is too high ({inference_time}s). It should only measure the predict() call."

    assert set(datasets_found) == set(EXPECTED_MSE.keys()), f"Missing results for datasets. Found: {datasets_found}"

def test_plots_exist():
    expected_plots = ["plot_data1.png", "plot_data2.png", "plot_data3.png"]
    for plot in expected_plots:
        plot_path = os.path.join(WORKSPACE_DIR, plot)
        assert os.path.isfile(plot_path), f"Plot file {plot_path} is missing."
        assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty."