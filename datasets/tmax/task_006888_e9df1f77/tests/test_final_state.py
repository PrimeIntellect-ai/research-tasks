# test_final_state.py

import os
import json
import stat
import subprocess
import pytest

def test_run_experiment_script_fixed():
    """Verify that run_experiment.py no longer uses TkAgg."""
    script_path = '/home/user/run_experiment.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "TkAgg" not in content, "The script still contains 'TkAgg' which requires a GUI."

def test_artifacts_generated():
    """Verify that results.json and plot.png were generated successfully."""
    results_path = '/home/user/results.json'
    plot_path = '/home/user/plot.png'

    assert os.path.isfile(results_path), f"Artifact {results_path} was not generated."
    assert os.path.isfile(plot_path), f"Artifact {plot_path} was not generated."
    assert os.path.getsize(plot_path) > 0, f"Artifact {plot_path} is empty."

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON.")

    assert 'accuracy' in data, "results.json is missing the 'accuracy' key."

def test_eval_script_exists_and_executable():
    """Verify that eval.sh exists and is executable."""
    eval_path = '/home/user/eval.sh'
    assert os.path.isfile(eval_path), f"Script {eval_path} does not exist."

    st = os.stat(eval_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {eval_path} is not executable."

def test_eval_script_behavior():
    """Verify that eval.sh correctly evaluates results.json."""
    eval_path = '/home/user/eval.sh'
    results_path = '/home/user/results.json'

    # First, test with the current results.json (should be PASS)
    result = subprocess.run([eval_path], capture_output=True, text=True)
    assert result.returncode == 0, f"eval.sh exited with code {result.returncode}, expected 0."
    assert result.stdout.strip() == "PASS", f"eval.sh outputted '{result.stdout.strip()}', expected 'PASS'."

    # Next, temporarily modify results.json to test the FAIL condition
    with open(results_path, 'r') as f:
        original_data = json.load(f)

    try:
        with open(results_path, 'w') as f:
            json.dump({"accuracy": 0.75, "loss": 0.5}, f)

        result_fail = subprocess.run([eval_path], capture_output=True, text=True)
        assert result_fail.returncode == 1, f"eval.sh exited with code {result_fail.returncode} for accuracy <= 0.80, expected 1."
        assert result_fail.stdout.strip() == "FAIL", f"eval.sh outputted '{result_fail.stdout.strip()}' for accuracy <= 0.80, expected 'FAIL'."
    finally:
        # Restore original results.json
        with open(results_path, 'w') as f:
            json.dump(original_data, f)