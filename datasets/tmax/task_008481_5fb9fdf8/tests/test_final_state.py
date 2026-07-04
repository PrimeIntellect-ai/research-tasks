# test_final_state.py

import os
import json
import csv
import math
import subprocess

def test_results_json_exists():
    """Test that the results.json file exists."""
    assert os.path.isfile('/home/user/results.json'), "The file /home/user/results.json does not exist."

def test_cargo_test_passes():
    """Test that the Rust project exists and cargo test passes."""
    project_dir = '/home/user/ab_test_pipeline'
    assert os.path.isdir(project_dir), f"The directory {project_dir} does not exist."

    cargo_toml = os.path.join(project_dir, 'Cargo.toml')
    assert os.path.isfile(cargo_toml), f"Cargo.toml not found in {project_dir}."

    try:
        result = subprocess.run(
            ['cargo', 'test'],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=60
        )
        assert result.returncode == 0, f"'cargo test' failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except FileNotFoundError:
        assert False, "cargo command not found. Is Rust installed?"

def test_results_json_values():
    """Test that the values in results.json match the derived metrics."""
    data_path = '/home/user/data.csv'
    assert os.path.isfile(data_path), f"Data file {data_path} missing."

    group_a_scores = []
    group_b_scores = []

    with open(data_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            duration = float(row['session_duration'])
            items = float(row['items_viewed'])
            score = (duration * 0.5) + (items * 2.5)
            if row['group'] == 'A':
                group_a_scores.append(score)
            elif row['group'] == 'B':
                group_b_scores.append(score)

    n_a = len(group_a_scores)
    n_b = len(group_b_scores)

    mean_a = sum(group_a_scores) / n_a
    mean_b = sum(group_b_scores) / n_b

    var_a = sum((x - mean_a) ** 2 for x in group_a_scores) / (n_a - 1)
    var_b = sum((x - mean_b) ** 2 for x in group_b_scores) / (n_b - 1)

    se = math.sqrt(var_a / n_a + var_b / n_b)
    t_stat = (mean_b - mean_a) / se

    with open('/home/user/results.json', 'r', encoding='utf-8') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, "results.json is not a valid JSON file."

    expected_keys = {"mean_a", "mean_b", "t_statistic", "p_value", "ci_lower", "ci_upper"}
    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"results.json is missing keys: {missing_keys}"

    assert math.isclose(results['mean_a'], mean_a, abs_tol=1e-3), f"mean_a expected ~{mean_a:.4f}, got {results['mean_a']}"
    assert math.isclose(results['mean_b'], mean_b, abs_tol=1e-3), f"mean_b expected ~{mean_b:.4f}, got {results['mean_b']}"
    assert math.isclose(results['t_statistic'], t_stat, abs_tol=1e-3), f"t_statistic expected ~{t_stat:.4f}, got {results['t_statistic']}"

    # Basic invariant checks for p-value and CI
    assert 0.0 <= results['p_value'] <= 1.0, f"p_value {results['p_value']} is out of bounds [0, 1]"
    assert results['ci_lower'] < results['ci_upper'], "ci_lower must be less than ci_upper"

    diff = mean_b - mean_a
    assert results['ci_lower'] < diff < results['ci_upper'], "Difference in means must be within the confidence interval"