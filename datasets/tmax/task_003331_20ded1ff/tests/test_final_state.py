# test_final_state.py
import os
import json
import math

def test_experiment_log():
    log_path = '/home/user/experiment_log.json'
    assert os.path.exists(log_path), f"Experiment log not found at {log_path}"

    with open(log_path, 'r') as f:
        try:
            log = json.load(f)
        except json.JSONDecodeError:
            assert False, "experiment_log.json is not valid JSON"

    assert 'optimal_components' in log, "Missing 'optimal_components' in experiment_log.json"
    assert 'reconstruction_max_error' in log, "Missing 'reconstruction_max_error' in experiment_log.json"

    # Based on the fixed random seed in the setup, the intrinsic dimensionality is 50.
    # The optimal components for >= 0.95 variance is exactly 50.
    assert log['optimal_components'] == 50, f"Expected 50 optimal components, got {log['optimal_components']}"

    # The reconstruction max error should be around 0.44
    max_error = log['reconstruction_max_error']
    assert isinstance(max_error, (int, float)), "reconstruction_max_error must be a number"
    assert 0.4 < max_error < 0.5, f"Expected reconstruction_max_error to be around 0.44, got {max_error}"

def test_hdf5_file_exists_and_valid():
    h5_path = '/home/user/reduced_features.h5'
    assert os.path.exists(h5_path), f"HDF5 file not found at {h5_path}"
    assert os.path.isfile(h5_path), f"{h5_path} is not a file"

    # Check HDF5 file signature (\x89HDF\r\n\x1a\n)
    with open(h5_path, 'rb') as f:
        header = f.read(8)
    expected_signature = b'\x89HDF\r\n\x1a\n'
    assert header == expected_signature, f"File {h5_path} is not a valid HDF5 file (invalid signature)"