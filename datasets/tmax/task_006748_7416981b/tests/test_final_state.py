# test_final_state.py

import os

def test_flat_dataset_directory_exists():
    flat_dir = "/home/user/flat_dataset"
    assert os.path.exists(flat_dir), f"Directory {flat_dir} does not exist."
    assert os.path.isdir(flat_dir), f"Path {flat_dir} is not a directory."

def test_flat_dataset_files_and_content():
    flat_dir = "/home/user/flat_dataset"
    assert os.path.exists(flat_dir), f"Directory {flat_dir} does not exist."

    expected_files = {
        "region_A_station_1_data_log.txt": "DATA_A1\n",
        "region_A_station_2_data_log.txt": "DATA_A2\n",
        "region_B_station_3_data_log.txt": "DATA_B3\n"
    }

    actual_files = set(os.listdir(flat_dir))
    expected_filenames = set(expected_files.keys())

    missing_files = expected_filenames - actual_files
    extra_files = actual_files - expected_filenames

    assert not missing_files, f"Missing expected files in {flat_dir}: {missing_files}"
    assert not extra_files, f"Found unexpected files in {flat_dir}: {extra_files}"

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(flat_dir, filename)
        with open(filepath, 'r') as f:
            content = f.read()
            assert content == expected_content, f"Content mismatch in {filename}. Expected '{expected_content}', got '{content}'."