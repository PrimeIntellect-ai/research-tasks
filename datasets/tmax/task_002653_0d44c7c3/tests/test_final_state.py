# test_final_state.py

import os
import pandas as pd
import numpy as np

def test_trajectory_csv_metric():
    """Evaluate the trajectory.csv file against the MSE threshold."""
    csv_path = "/home/user/trajectory.csv"
    assert os.path.isfile(csv_path), f"Missing output CSV at {csv_path}"

    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        assert False, f"Failed to read {csv_path} as CSV: {e}"

    assert 'distance_to_center' in df.columns, f"Missing column 'distance_to_center' in {csv_path}"

    distances = df['distance_to_center'].dropna().values
    assert len(distances) > 0, "No valid data rows found in trajectory.csv"

    gt_distances = np.full_like(distances, 30.0)
    mse = np.mean((distances - gt_distances) ** 2)

    assert mse <= 2.5, f"MSE of distance_to_center is {mse:.4f}, which exceeds the threshold of 2.5"

def test_etl_pipeline_script_exists():
    """Check if the ETL pipeline bash script exists."""
    script_path = "/home/user/etl_pipeline.sh"
    assert os.path.isfile(script_path), f"Missing bash script at {script_path}"

def test_cron_schedule_content():
    """Check if the cron schedule file exists and has the correct schedule."""
    cron_path = "/home/user/cron_schedule.txt"
    assert os.path.isfile(cron_path), f"Missing cron schedule file at {cron_path}"

    with open(cron_path, "r") as f:
        content = f.read().strip()

    assert "*/5 * * * *" in content, f"Cron schedule does not contain the correct interval '*/5 * * * *'. Content: {content}"
    assert "/home/user/etl_pipeline.sh" in content, f"Cron schedule does not contain the script path. Content: {content}"

def test_cpp_source_exists():
    """Check if the C++ source file exists."""
    cpp_path = "/home/user/process_radar.cpp"
    assert os.path.isfile(cpp_path), f"Missing C++ source file at {cpp_path}"