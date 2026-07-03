# test_final_state.py
import os
import csv
import subprocess

def test_venv_and_numpy():
    venv_python = "/home/user/prep_env/bin/python"
    assert os.path.isfile(venv_python), "Virtual environment Python executable not found at /home/user/prep_env/bin/python"

    result = subprocess.run([venv_python, "-c", "import numpy"], capture_output=True)
    assert result.returncode == 0, "numpy is not installed in the virtual environment at /home/user/prep_env"

def test_script_exists():
    assert os.path.isfile("/home/user/preprocess.py"), "/home/user/preprocess.py is missing"

def test_features_csv():
    csv_path = "/home/user/features.csv"
    assert os.path.isfile(csv_path), f"{csv_path} is missing"

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) == 4, "features.csv should have exactly 4 rows (1 header + 3 data rows)"

    header = rows[0]
    expected_header = ["pdb_id", "seq_length", "com_x", "com_y", "com_z", "max_norm_dist"]
    assert header == expected_header, f"Header mismatch. Expected {expected_header}, got {header}"

    expected_data = [
        ["1abc", "3", "10.0000", "11.3333", "11.0000", "5.8466"],
        ["2xyz", "1", "5.0000", "5.0000", "5.0000", "0.0000"],
        ["3mno", "20", "1.0000", "0.0000", "0.0000", "100000000.0000"]
    ]

    data = rows[1:]
    assert data == expected_data, f"Data mismatch. Expected {expected_data}, got {data}"