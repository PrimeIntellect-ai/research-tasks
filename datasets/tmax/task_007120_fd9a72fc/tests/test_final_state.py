# test_final_state.py
import os
import json
import subprocess
import pytest

def test_joined_data():
    joined_path = '/home/user/output/joined_data.csv'
    assert os.path.isfile(joined_path), f"{joined_path} does not exist."

    with open(joined_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 11, f"Expected 11 lines in joined_data.csv, found {len(lines)}."
    assert lines[0] == 'id,feature1,feature2,feature3,target', f"Incorrect header in joined_data.csv: {lines[0]}"

    # Check a specific line to ensure join was correct
    assert '1,0.5,1.2,3.3,10.1' in lines, "Joined data does not contain expected row for id=1."

def test_analyze_script_modifications():
    script_path = '/home/user/scripts/analyze.py'
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'plt.show()' not in content, "analyze.py still contains plt.show(), which fails in headless environments."
    assert 'correlation.png' in content, "analyze.py does not appear to save the plot to correlation.png."
    assert '42' in content, "analyze.py does not appear to use random seed 42."

def test_correlation_plot_exists():
    plot_path = '/home/user/output/correlation.png'
    assert os.path.isfile(plot_path), f"{plot_path} does not exist."
    assert os.path.getsize(plot_path) > 0, f"{plot_path} is empty."

def test_metrics_json():
    json_path = '/home/user/output/metrics.json'
    assert os.path.isfile(json_path), f"{json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not valid JSON.")

    assert 'pca_variance' in data, "metrics.json is missing 'pca_variance' key."
    assert 'r2_score' in data, "metrics.json is missing 'r2_score' key."
    assert isinstance(data['pca_variance'], float), "'pca_variance' must be a float."
    assert isinstance(data['r2_score'], float), "'r2_score' must be a float."

def test_reproducibility_script():
    script_path = '/home/user/test_reproducibility.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    # Run the reproducibility test script
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"test_reproducibility.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"