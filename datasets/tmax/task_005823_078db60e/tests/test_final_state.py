# test_final_state.py
import os
import json
import pytest

def test_experiment_results_json():
    json_path = "/home/user/experiment_results.json"
    assert os.path.isfile(json_path), f"Expected log file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    expected_keys = {
        "time_1_thread",
        "time_4_threads",
        "explained_variance_ratio_sum",
        "num_raw_vectors",
        "num_clean_vectors"
    }

    missing_keys = expected_keys - set(data.keys())
    assert not missing_keys, f"JSON is missing keys: {missing_keys}"

    assert isinstance(data["time_1_thread"], (int, float)), "time_1_thread must be a number"
    assert data["time_1_thread"] > 0, "time_1_thread must be > 0"

    assert isinstance(data["time_4_threads"], (int, float)), "time_4_threads must be a number"
    assert data["time_4_threads"] > 0, "time_4_threads must be > 0"

    assert isinstance(data["explained_variance_ratio_sum"], (int, float)), "explained_variance_ratio_sum must be a number"
    assert 0 < data["explained_variance_ratio_sum"] <= 1.0, "explained_variance_ratio_sum must be between 0 and 1"

    assert data["num_raw_vectors"] == 5000, f"Expected num_raw_vectors to be 5000, got {data['num_raw_vectors']}"
    assert data["num_clean_vectors"] == 4900, f"Expected num_clean_vectors to be 4900, got {data['num_clean_vectors']}"

def test_clean_embeddings_file():
    clean_path = "/home/user/clean_embeddings.npy"
    assert os.path.isfile(clean_path), f"Expected clean embeddings file {clean_path} does not exist."

    # Check file size to ensure it matches 4900 vectors of 512 float32s
    # 4900 * 512 * 4 bytes = 10035200 bytes. With .npy header (typically 128 bytes), it should be slightly larger.
    file_size = os.path.getsize(clean_path)
    expected_data_size = 4900 * 512 * 4

    assert file_size >= expected_data_size, f"File size {file_size} is too small to contain 4900 vectors of 512 float32s."
    assert file_size < expected_data_size + 1024, f"File size {file_size} is too large, expected around {expected_data_size} bytes."