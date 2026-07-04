# test_final_state.py
import os
import csv

def test_scripts_exist_and_executable():
    python_script = "/home/user/clean_metrics.py"
    bash_script = "/home/user/run_pipeline.sh"

    assert os.path.exists(python_script), f"{python_script} does not exist."
    assert os.path.isfile(python_script), f"{python_script} is not a file."

    assert os.path.exists(bash_script), f"{bash_script} does not exist."
    assert os.path.isfile(bash_script), f"{bash_script} is not a file."
    assert os.access(bash_script, os.X_OK), f"{bash_script} is not executable."

def test_venv_exists():
    venv_dir = "/home/user/venv"
    assert os.path.exists(venv_dir), f"Virtual environment directory {venv_dir} does not exist."
    assert os.path.isdir(venv_dir), f"{venv_dir} is not a directory."

    python_bin = os.path.join(venv_dir, "bin", "python")
    assert os.path.exists(python_bin), f"Python executable not found in {venv_dir}/bin/python."

def test_clean_metrics_csv_content():
    csv_file = "/home/user/clean_metrics.csv"
    assert os.path.exists(csv_file), f"{csv_file} does not exist."
    assert os.path.isfile(csv_file), f"{csv_file} is not a file."

    expected_data = [
        {"timestamp": "2023-10-01T10:00:00", "cpu_usage": 45.2, "memory_usage": 1000.0, "response_time": 120.0},
        {"timestamp": "2023-10-01T10:02:00", "cpu_usage": 40.1, "memory_usage": 2000.0, "response_time": 110.0},
        {"timestamp": "2023-10-01T10:04:00", "cpu_usage": 60.5, "memory_usage": 3000.0, "response_time": 140.0},
        {"timestamp": "2023-10-01T10:06:00", "cpu_usage": 55.0, "memory_usage": 4000.0, "response_time": 180.0},
    ]

    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == len(expected_data), f"Expected {len(expected_data)} rows in {csv_file}, but found {len(rows)}."

    for i, (actual, expected) in enumerate(zip(rows, expected_data)):
        assert actual["timestamp"] == expected["timestamp"], f"Row {i+1}: expected timestamp {expected['timestamp']}, got {actual.get('timestamp')}"

        try:
            cpu = float(actual["cpu_usage"])
            mem = float(actual["memory_usage"])
            resp = float(actual["response_time"])
        except (ValueError, KeyError) as e:
            assert False, f"Row {i+1}: error parsing numerical values: {e}"

        assert abs(cpu - expected["cpu_usage"]) < 1e-6, f"Row {i+1}: expected cpu_usage {expected['cpu_usage']}, got {cpu}"
        assert abs(mem - expected["memory_usage"]) < 1e-6, f"Row {i+1}: expected memory_usage {expected['memory_usage']}, got {mem}"
        assert abs(resp - expected["response_time"]) < 1e-6, f"Row {i+1}: expected response_time {expected['response_time']}, got {resp}"