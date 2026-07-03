# test_final_state.py
import os
import json

def test_json_results():
    json_path = '/home/user/test_results.json'
    assert os.path.exists(json_path), f"JSON results file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    assert 'test_accuracy' in res, "The key 'test_accuracy' is missing in the JSON file."
    assert isinstance(res['test_accuracy'], float), "The value of 'test_accuracy' must be a float."

def test_mlflow_tracking():
    mlruns_dir = '/home/user/mlruns'
    assert os.path.isdir(mlruns_dir), f"MLflow tracking directory {mlruns_dir} is missing."

    # Find experiment ID for 'Sensor_Failure_Exp'
    exp_id = None
    for item in os.listdir(mlruns_dir):
        exp_dir = os.path.join(mlruns_dir, item)
        if os.path.isdir(exp_dir):
            meta_path = os.path.join(exp_dir, 'meta.yaml')
            if os.path.exists(meta_path):
                with open(meta_path, 'r') as f:
                    content = f.read()
                    if 'name: Sensor_Failure_Exp' in content:
                        exp_id = item
                        break

    assert exp_id is not None, "Experiment 'Sensor_Failure_Exp' not found in mlruns."

    exp_dir = os.path.join(mlruns_dir, exp_id)
    # Find run directories
    run_dirs = [d for d in os.listdir(exp_dir) if os.path.isdir(os.path.join(exp_dir, d)) and d != '.trash']
    assert len(run_dirs) > 0, "No MLflow runs found for the experiment."

    # Verify that at least one run has the correct properties
    success = False
    for run_id in run_dirs:
        run_dir = os.path.join(exp_dir, run_id)

        # Check param n_estimators
        param_path = os.path.join(run_dir, 'params', 'n_estimators')
        if not os.path.exists(param_path): 
            continue
        with open(param_path, 'r') as f:
            if f.read().strip() != '50': 
                continue

        # Check metric test_accuracy
        metric_path = os.path.join(run_dir, 'metrics', 'test_accuracy')
        if not os.path.exists(metric_path): 
            continue

        # Check tag pipeline_version
        tag_path = os.path.join(run_dir, 'tags', 'pipeline_version')
        if not os.path.exists(tag_path): 
            continue
        with open(tag_path, 'r') as f:
            if f.read().strip() != 'v1.0': 
                continue

        # Check artifact rf_model
        artifact_dir = os.path.join(run_dir, 'artifacts', 'rf_model')
        if not os.path.isdir(artifact_dir): 
            continue

        success = True
        break

    assert success, "Could not find an MLflow run with the correct parameters, metrics, tags, and artifacts."