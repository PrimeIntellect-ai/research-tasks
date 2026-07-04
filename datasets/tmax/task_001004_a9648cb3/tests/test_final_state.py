# test_final_state.py
import os
import csv

def test_result_file_exists():
    """Test that the result.txt file exists."""
    file_path = "/home/user/result.txt"
    assert os.path.exists(file_path), f"The result file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_result_file_format_and_content():
    """Test that the result.txt file contains exactly 3 valid sensor IDs."""
    result_path = "/home/user/result.txt"
    dataset_path = "/home/user/sensor_data.csv"

    assert os.path.exists(result_path), "Cannot check format because result.txt is missing."
    assert os.path.exists(dataset_path), "Cannot validate sensors because sensor_data.csv is missing."

    with open(result_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 sensor IDs in result.txt, but found {len(lines)}."

    # Extract valid sensor IDs from the dataset
    with open(dataset_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        valid_sensors = set(row[0] for row in reader if row)

    for sensor in lines:
        assert sensor in valid_sensors, f"Output contains invalid sensor ID: '{sensor}'."
        assert sensor != "sensor_0", "The results should exclude 'sensor_0' itself."

    # Ensure no duplicates in the output
    assert len(set(lines)) == 3, "The result.txt file contains duplicate sensor IDs."