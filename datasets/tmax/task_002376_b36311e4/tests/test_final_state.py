# test_final_state.py

import os

def test_validate_stability_script_exists_and_executable():
    """Check if validate_stability.sh exists and is executable."""
    file_path = "/home/user/validate_stability.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing."
    assert os.access(file_path, os.X_OK), f"File {file_path} is not executable."

def test_venv_directory_exists():
    """Check if the Python virtual environment directory exists."""
    dir_path = "/home/user/venv"
    assert os.path.isdir(dir_path), f"Virtual environment directory {dir_path} is missing."
    assert os.path.isfile(os.path.join(dir_path, "bin", "python")), "Python interpreter missing in venv."

def test_output_csv_exists():
    """Check if output.csv was generated during execution."""
    file_path = "/home/user/sim_env/output.csv"
    assert os.path.isfile(file_path), f"Simulation output file {file_path} is missing."

def test_stability_report_content():
    """Check if stability_report.txt exists and contains the correct average frequency."""
    file_path = "/home/user/stability_report.txt"
    assert os.path.isfile(file_path), f"Report file {file_path} is missing."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    expected_content = "Average Frequency: 2.530 Hz"
    assert content == expected_content, f"Content of {file_path} is incorrect. Expected '{expected_content}', got '{content}'."