# test_final_state.py

import os
import glob
import importlib.util
import pytest

def test_run_pipeline_script_exists_and_executable():
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_graph_factor_lib_installed():
    # Attempt to import the library to verify it was installed successfully
    spec = importlib.util.find_spec("graph_factor_lib")
    assert spec is not None, "The package 'graph_factor_lib' is not installed in the active Python environment."

def test_notebooks_out_generated():
    out_dir = '/home/user/notebooks_out'
    assert os.path.isdir(out_dir), f"The directory {out_dir} does not exist."

    data_dir = '/home/user/data'
    edges_files = glob.glob(os.path.join(data_dir, '*.edges'))

    for edge_file in edges_files:
        basename = os.path.splitext(os.path.basename(edge_file))[0]
        expected_notebook = os.path.join(out_dir, f"{basename}_out.ipynb")
        assert os.path.isfile(expected_notebook), f"Expected output notebook {expected_notebook} was not generated."

def test_final_mean_kl_metric():
    metric_file = '/home/user/final_mean_kl.txt'
    assert os.path.isfile(metric_file), f"The file {metric_file} does not exist."

    with open(metric_file, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse the content of {metric_file} as a float. Content: '{content}'")

    threshold = 0.05
    assert val <= threshold, f"The mean KL divergence ({val}) is greater than the threshold ({threshold})."