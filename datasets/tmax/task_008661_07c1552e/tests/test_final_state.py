# test_final_state.py
import os
import subprocess

def test_venv_exists():
    python_path = "/home/user/sensor_env/bin/python"
    assert os.path.isfile(python_path), f"Virtual environment python not found at {python_path}"

def test_processed_sensors_dir():
    target_dir = "/home/user/processed_sensors"
    assert os.path.isdir(target_dir), f"Directory {target_dir} does not exist"

def test_partitions_exist():
    for sensor in ["A", "B", "C"]:
        part_dir = f"/home/user/processed_sensors/sensor_id={sensor}"
        assert os.path.isdir(part_dir), f"Partition directory {part_dir} does not exist"
        files = os.listdir(part_dir)
        assert any(f.endswith('.parquet') for f in files), f"No .parquet files found in {part_dir}"

def test_data_correctness():
    # We use the student's virtual environment which should have pandas and pyarrow installed
    python_path = "/home/user/sensor_env/bin/python"

    script = """
import sys
try:
    import pandas as pd
except ImportError:
    print("pandas is not installed in the virtual environment")
    sys.exit(1)

try:
    df = pd.read_parquet("/home/user/processed_sensors")
except Exception as e:
    print(f"Error reading parquet dataset: {e}")
    sys.exit(1)

# Check no NaNs
if df.isna().sum().sum() != 0:
    print("There are missing values in the dataset")
    sys.exit(1)

# Check row count
if len(df) != 980:
    print(f"Expected 980 rows, got {len(df)}")
    sys.exit(1)

# Check clipping
if df['temperature'].max() >= 50:
    print("Temperature outliers were not capped")
    sys.exit(1)
if df['temperature'].min() <= -50:
    print("Temperature outliers were not floored")
    sys.exit(1)
if df['humidity'].max() >= 150:
    print("Humidity outliers were not capped")
    sys.exit(1)
if df['humidity'].min() <= -50:
    print("Humidity outliers were not floored")
    sys.exit(1)

print("OK")
sys.exit(0)
"""
    result = subprocess.run(
        [python_path, "-c", script],
        capture_output=True,
        text=True
    )

    error_msg = result.stdout.strip() if result.stdout.strip() != "" else result.stderr.strip()
    assert result.returncode == 0, f"Data validation failed: {error_msg}"