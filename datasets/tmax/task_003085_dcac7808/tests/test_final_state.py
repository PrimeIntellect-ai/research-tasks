# test_final_state.py

import os
import re

def test_processed_dataset_directory():
    """Check if the processed_dataset directory exists."""
    dir_path = "/home/user/processed_dataset"
    assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

def test_processed_files_exist():
    """Check if the renamed .dat files exist in the target directory."""
    dir_path = "/home/user/processed_dataset"
    for i in range(1, 11):
        filename = f"sensor_X{i}_17000000{i:02d}.dat"
        file_path = os.path.join(dir_path, filename)
        assert os.path.isfile(file_path), f"Expected processed file {file_path} does not exist."

def test_rename_log_exists_and_format():
    """Check if rename_log.txt exists, has 10 lines, and follows the correct format."""
    log_path = "/home/user/processed_dataset/rename_log.txt"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 10, f"Expected exactly 10 lines in {log_path}, found {len(lines)}."

    # Check that each expected file mapping is present
    expected_mappings = []
    for i in range(1, 11):
        orig = f"file_{i:02d}.dat"
        new = f"sensor_X{i}_17000000{i:02d}.dat"
        expected_mappings.append(f"{orig} -> {new}")

    for mapping in expected_mappings:
        assert mapping in lines, f"Expected mapping '{mapping}' not found in {log_path}."

def test_process_data_script():
    """Check if process_data.py exists and contains the required keywords."""
    script_path = "/home/user/process_data.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    # Check for filelock usage
    assert "filelock" in content.lower(), f"Script {script_path} must use the filelock package."

    # Check for concurrency usage
    has_concurrent = "concurrent" in content or "multiprocessing" in content
    assert has_concurrent, f"Script {script_path} must use concurrent.futures or multiprocessing."

def test_filelock_installed():
    """Check if the filelock package is installed in the environment."""
    try:
        import filelock
    except ImportError:
        assert False, "The 'filelock' package is not installed."