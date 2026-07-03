# test_final_state.py
import os
import subprocess
import pytest

def test_pipeline_script_exists():
    pipeline_path = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_path), f"The pipeline script {pipeline_path} does not exist."
    assert os.access(pipeline_path, os.X_OK), f"The pipeline script {pipeline_path} is not executable."

def test_output_manifests_generated():
    output_dir = "/home/user/output_manifests"
    assert os.path.isdir(output_dir), f"The output directory {output_dir} does not exist."
    files = [f for f in os.listdir(output_dir) if f.endswith(('.yaml', '.yml'))]
    assert len(files) > 0, f"No YAML files found in {output_dir}. The Rust processor did not generate outputs."

def test_manifest_accuracy_metric():
    eval_script = "/home/user/evaluate_manifests.py"
    assert os.path.isfile(eval_script), f"The evaluator script {eval_script} is missing."

    try:
        result = subprocess.run(
            ["python3", eval_script, "--metric-only"],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Evaluator script failed to run. stderr: {e.stderr}")

    output = result.stdout.strip()
    try:
        metric_value = float(output)
    except ValueError:
        pytest.fail(f"Evaluator script did not output a valid float. Output was: '{output}'")

    threshold = 0.95
    assert metric_value >= threshold, (
        f"Manifest accuracy metric is {metric_value}, which is below the required threshold of {threshold}. "
        "Ensure the Rust program correctly parses and applies all rules from the image."
    )