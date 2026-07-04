# test_final_state.py
import os
import csv

def test_script_exists_and_executable():
    script_path = "/home/user/run_regression.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_executed_notebook_exists():
    notebook_path = "/home/user/sim_project/diffusion_executed.ipynb"
    assert os.path.isfile(notebook_path), f"Executed notebook {notebook_path} is missing."

def test_test_dist_csv_exists_and_valid():
    csv_path = "/home/user/sim_project/test_dist.csv"
    assert os.path.isfile(csv_path), f"Output CSV {csv_path} is missing."

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['node', 'prob'], "CSV header is incorrect; expected 'node,prob'."
        rows = list(reader)
        assert len(rows) == 8, f"Expected 8 rows in CSV, found {len(rows)}."

def test_regression_result_log():
    log_path = "/home/user/regression_result.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content == "TVD=0.0124", f"Log file content is incorrect. Expected 'TVD=0.0124', got '{content}'."