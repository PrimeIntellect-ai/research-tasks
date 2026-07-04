# test_final_state.py

import os
import json
import subprocess

def test_venv_exists():
    venv_python = '/home/user/venv/bin/python'
    assert os.path.exists(venv_python), f"Virtual environment Python not found at {venv_python}"

def test_dependencies_installed():
    venv_python = '/home/user/venv/bin/python'
    assert os.path.exists(venv_python), "Virtual environment not found."

    # Check scikit-learn version
    result = subprocess.run(
        [venv_python, '-c', 'import sklearn; print(sklearn.__version__)'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, "Failed to import sklearn in the venv."
    assert result.stdout.strip() == "1.3.2", f"Expected scikit-learn==1.3.2, but got {result.stdout.strip()}"

    # Check pandas
    result_pd = subprocess.run(
        [venv_python, '-c', 'import pandas'],
        capture_output=True, text=True
    )
    assert result_pd.returncode == 0, "Failed to import pandas in the venv."

def test_script_exists():
    script_path = '/home/user/run_analysis.py'
    assert os.path.exists(script_path), f"Analysis script not found at {script_path}"

def test_experiment_log_valid():
    log_path = '/home/user/experiment_log.json'
    assert os.path.exists(log_path), f"Experiment log not found at {log_path}"

    with open(log_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "Experiment log is not valid JSON."

    assert "pca_explained_variance_ratio_sum" in data, "Missing 'pca_explained_variance_ratio_sum' in log."
    assert "bgm_lower_bound" in data, "Missing 'bgm_lower_bound' in log."
    assert "bgm_converged" in data, "Missing 'bgm_converged' in log."

    assert data["bgm_converged"] is True, f"Expected bgm_converged to be True, got {data['bgm_converged']}"

    pca_var = data["pca_explained_variance_ratio_sum"]
    assert isinstance(pca_var, float), "pca_explained_variance_ratio_sum must be a float."
    assert 0.70 < pca_var < 0.80, f"pca_explained_variance_ratio_sum {pca_var} is out of expected range (0.70 - 0.80)."

    bgm_lb = data["bgm_lower_bound"]
    assert isinstance(bgm_lb, float), "bgm_lower_bound must be a float."
    assert -5.0 < bgm_lb < -3.0, f"bgm_lower_bound {bgm_lb} is out of expected range (-5.0 - -3.0)."