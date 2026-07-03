# test_final_state.py
import os
import stat
import time
import json
import subprocess

def test_directories_exist():
    """Verify that the required directories have been created."""
    assert os.path.isdir("/home/user/raw_datasets"), "/home/user/raw_datasets directory does not exist."
    assert os.path.isdir("/home/user/clean_datasets"), "/home/user/clean_datasets directory does not exist."

def test_script_exists_and_executable():
    """Verify that the auto_process.sh script exists and is executable."""
    script_path = "/home/user/auto_process.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_script_is_running():
    """Verify that the script is running in the background."""
    try:
        ps_output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    except subprocess.CalledProcessError:
        assert False, "Failed to run 'ps aux' to check running processes."

    assert "auto_process.sh" in ps_output, "The script auto_process.sh does not appear to be running in the background."

def test_processing_behavior():
    """Verify the file watching and TSV to JSON conversion logic."""
    tsv_data = "SampleID\tMeasurement\tTimestamp\nX-100\t99.9\t2023-11-01T12:00:00Z\nY-200\t-4.5\t2023-11-01T12:05:00Z\n"
    input_path = "/home/user/raw_datasets/test_experiment_99.tsv"
    output_path = "/home/user/clean_datasets/test_experiment_99.json"

    # Ensure a clean slate for the test
    if os.path.exists(output_path):
        os.remove(output_path)

    # Write the test TSV in UTF-16LE
    with open(input_path, "w", encoding="utf-16le") as f:
        f.write(tsv_data)

    # Wait for processing (up to 5 seconds)
    timeout = 5.0
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(output_path):
            break
        time.sleep(0.5)

    assert os.path.exists(output_path), f"Output file {output_path} was not created within {timeout} seconds."

    # Verify output
    with open(output_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Output file {output_path} does not contain valid JSON."

    expected_data = [
        {"SampleID": "X-100", "Measurement": "99.9", "Timestamp": "2023-11-01T12:00:00Z"},
        {"SampleID": "Y-200", "Measurement": "-4.5", "Timestamp": "2023-11-01T12:05:00Z"}
    ]

    assert data == expected_data, f"Data mismatch. Expected {expected_data}, got {data}"