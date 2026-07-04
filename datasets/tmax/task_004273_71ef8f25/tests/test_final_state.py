# test_final_state.py
import os
import json
import stat
import hashlib

def test_run_pipeline_script_exists_and_executable():
    """Check that run_pipeline.sh exists and is executable."""
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_venv_exists():
    """Check that the virtual environment was created."""
    venv_path = '/home/user/venv'
    assert os.path.isdir(venv_path), f"Virtual environment not found at {venv_path}."
    python_bin = os.path.join(venv_path, 'bin', 'python')
    assert os.path.isfile(python_bin) or os.path.isfile(os.path.join(venv_path, 'bin', 'python3')), "Python executable not found in venv."

def test_metrics_json():
    """Check that metrics.json exists, is valid JSON, and MAE is < 50.0."""
    metrics_path = '/home/user/metrics.json'
    assert os.path.isfile(metrics_path), f"{metrics_path} does not exist."

    with open(metrics_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{metrics_path} does not contain valid JSON."

    assert "mae" in data, f"'mae' key missing in {metrics_path}."
    assert isinstance(data["mae"], (int, float)), f"'mae' is not a number in {metrics_path}."
    assert data["mae"] < 50.0, f"MAE is {data['mae']}, which is not less than 50.0."

def test_residuals_plot():
    """Check that residuals.png exists and is not a blank canvas."""
    plot_path = '/home/user/residuals.png'
    assert os.path.isfile(plot_path), f"{plot_path} does not exist."

    # A blank matplotlib figure is typically around 1-3KB. 
    # A real scatter plot with 400 points will be > 5KB.
    file_size = os.path.getsize(plot_path)
    assert file_size > 5000, f"{plot_path} is too small ({file_size} bytes), indicating it might be blank."

def test_generate_data_unmodified():
    """Check that generate_data.py was not modified."""
    gen_path = '/home/user/generate_data.py'
    assert os.path.isfile(gen_path), f"{gen_path} does not exist."

    # Compute SHA256 of the original file
    original_content = """import numpy as np
import pandas as pd

def generate():
    np.random.seed(42)
    n_samples = 2000

    # Feature 1: Very large scale (e.g., pressure in Pascals)
    X1 = np.random.uniform(10000, 50000, n_samples)

    # Feature 2: Very small scale (e.g., friction coefficient)
    X2 = np.random.uniform(0.001, 0.005, n_samples)

    # Target variable
    y = 0.05 * X1 + 15000 * X2 + np.random.normal(0, 10, n_samples)

    df = pd.DataFrame({'pressure': X1, 'friction': X2, 'target': y})
    df.to_csv('/home/user/data.csv', index=False)
    print("Data generated at /home/user/data.csv")

if __name__ == "__main__":
    generate()
"""
    with open(gen_path, 'r') as f:
        current_content = f.read()

    assert current_content == original_content, f"{gen_path} was modified."