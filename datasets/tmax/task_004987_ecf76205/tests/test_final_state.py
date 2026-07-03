# test_final_state.py

import json
import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/rust-etl"
METRICS_FILE = os.path.join(PROJECT_DIR, "metrics.json")
PLOT_FILE = os.path.join(PROJECT_DIR, "plot.png")
MAIN_RS = os.path.join(PROJECT_DIR, "src/main.rs")

def test_metrics_json_valid_and_mse_low():
    assert os.path.exists(METRICS_FILE), f"{METRICS_FILE} not found. Did you output the metrics?"

    with open(METRICS_FILE, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{METRICS_FILE} is not a valid JSON file.")

    assert "mse" in data, "The key 'mse' is missing in metrics.json."
    mse_value = data["mse"]
    assert isinstance(mse_value, (int, float)), "The value of 'mse' must be a number."
    assert mse_value < 2.0, f"MSE is {mse_value}, but it should be < 2.0. Did you adjust n_components correctly?"

def test_plot_png_valid():
    assert os.path.exists(PLOT_FILE), f"{PLOT_FILE} not found. Did you generate the plot?"

    size = os.path.getsize(PLOT_FILE)
    assert size > 1000, f"{PLOT_FILE} is too small ({size} bytes). The plotting logic is likely not finalized properly (e.g., missing .present() or drop)."

    with open(PLOT_FILE, 'rb') as f:
        header = f.read(8)
    assert header == b'\x89PNG\r\n\x1a\n', f"{PLOT_FILE} does not have a valid PNG header. It might be corrupted."

def test_cargo_test_passes():
    assert os.path.exists(PROJECT_DIR), f"{PROJECT_DIR} does not exist."

    result = subprocess.run(
        ["cargo", "test"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    assert result.returncode == 0, f"'cargo test' failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

def test_n_components_adjusted():
    assert os.path.exists(MAIN_RS), f"{MAIN_RS} not found."

    with open(MAIN_RS, 'r') as f:
        content = f.read()

    # Just a sanity check that n_components(1) was removed or changed
    # We won't strictly parse the AST, but we can verify that n_components(1) is not present
    # and some n_components(X) where X >= 3 is present.
    import re
    matches = re.findall(r'n_components\s*\(\s*(\d+)\s*\)', content)
    assert matches, "Could not find 'n_components(...)' in src/main.rs"

    # Check if any of the matches is >= 3
    valid_components = any(int(m) >= 3 for m in matches)
    assert valid_components, "n_components must be set to a value >= 3 to achieve the required accuracy."