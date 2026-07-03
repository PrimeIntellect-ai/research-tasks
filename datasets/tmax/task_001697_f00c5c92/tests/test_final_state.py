# test_final_state.py

import os
import json
import csv

WORKSPACE_DIR = "/home/user/workspace"
BENCHMARK_CSV = os.path.join(WORKSPACE_DIR, "benchmark.csv")
BENCHMARK_PNG = os.path.join(WORKSPACE_DIR, "benchmark.png")
EXPERIMENT_LOG = os.path.join(WORKSPACE_DIR, "experiment_log.json")
PLOT_SCRIPT = os.path.join(WORKSPACE_DIR, "plot.py")

def test_benchmark_csv_exists_and_valid():
    assert os.path.isfile(BENCHMARK_CSV), f"{BENCHMARK_CSV} is missing."

    with open(BENCHMARK_CSV, "r") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["batch_size", "time_seconds"], f"Incorrect columns in {BENCHMARK_CSV}: {header}"

        rows = list(reader)
        assert len(rows) == 3, f"Expected exactly 3 data rows in {BENCHMARK_CSV}, found {len(rows)}"

        try:
            batch_sizes = [int(row[0]) for row in rows]
        except ValueError:
            assert False, "Batch sizes in the CSV must be integers."

        assert batch_sizes == [1, 32, 128], f"Expected batch sizes [1, 32, 128] in ascending order, found {batch_sizes}"

        for row in rows:
            try:
                float(row[1])
            except ValueError:
                assert False, f"Time value '{row[1]}' in {BENCHMARK_CSV} is not a valid float."

def test_benchmark_png_exists_and_valid():
    assert os.path.isfile(BENCHMARK_PNG), f"{BENCHMARK_PNG} is missing."

    with open(BENCHMARK_PNG, "rb") as f:
        header = f.read(8)
        assert header == b'\x89PNG\r\n\x1a\n', f"{BENCHMARK_PNG} is not a valid PNG file."

def test_experiment_log_exists_and_valid():
    assert os.path.isfile(EXPERIMENT_LOG), f"{EXPERIMENT_LOG} is missing."

    with open(EXPERIMENT_LOG, "r") as f:
        try:
            log = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{EXPERIMENT_LOG} is not a valid JSON file."

    assert isinstance(log, dict), f"Expected JSON root to be a dictionary, found {type(log).__name__}"
    expected_keys = {"1", "32", "128"}
    assert set(log.keys()) == expected_keys, f"Expected keys {expected_keys} in {EXPERIMENT_LOG}, found {set(log.keys())}"

    for k in expected_keys:
        assert isinstance(log[k], (float, int)), f"Time value for key '{k}' in {EXPERIMENT_LOG} should be a number, found {type(log[k]).__name__}"

def test_plot_script_fixed():
    assert os.path.isfile(PLOT_SCRIPT), f"{PLOT_SCRIPT} is missing."

    with open(PLOT_SCRIPT, "r") as f:
        content = f.read()

    assert "plt.show()" not in content, "plot.py still contains 'plt.show()', which will fail in a headless environment."
    assert "benchmark.png" in content, "plot.py does not seem to contain the filename 'benchmark.png' to save the plot."