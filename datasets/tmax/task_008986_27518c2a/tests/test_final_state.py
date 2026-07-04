# test_final_state.py

import os
import subprocess
import pytest

def test_script_exists_and_executable():
    """Test if the clean_data.sh script exists and is executable."""
    script_path = "/home/user/clean_data.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_script_output():
    """Test if the script produces the correct CSV output."""
    script_path = "/home/user/clean_data.sh"
    output_csv = "/home/user/clean_sensors.csv"

    # Run the script to generate/overwrite the output file
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    assert os.path.isfile(output_csv), f"Output file {output_csv} was not created."

    expected_csv = """SensorID,Timestamp,X,Y,Distance
Sensor-E5,2024-01-05T10:15:00,7,8,15
Sensor-A1,2024-01-05T14:30:00,12,-5,17
Sensor-B2,2024-01-05T14:35:00,-10,20,30
Sensor-D4,2024-01-05T14:45:00,0,0,0"""

    with open(output_csv, "r") as f:
        actual_csv = f.read().strip()

    assert actual_csv == expected_csv, f"Content of {output_csv} does not match expected output.\nExpected:\n{expected_csv}\n\nActual:\n{actual_csv}"