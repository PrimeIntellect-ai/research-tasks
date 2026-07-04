# test_final_state.py
import os
import json
import tarfile
import tempfile
import pytest

def test_valid_data_jsonl_exists():
    valid_data_path = "/home/user/mlops/valid_data.jsonl"
    assert os.path.isfile(valid_data_path), f"{valid_data_path} is missing."

    with open(valid_data_path, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) > 0, f"{valid_data_path} is empty."

    for i, line in enumerate(lines):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            pytest.fail(f"Line {i+1} in {valid_data_path} is not valid JSON.")

        assert "log_id" in record, f"Missing 'log_id' in line {i+1}"
        assert "message" in record, f"Missing 'message' in line {i+1}"
        assert "features" in record, f"Missing 'features' in line {i+1}"
        assert "recovery_time" in record, f"Missing 'recovery_time' in line {i+1}"
        assert isinstance(record["features"], list) and len(record["features"]) == 2, f"'features' is not a list of 2 items in line {i+1}"

@pytest.fixture(scope="module")
def extracted_artifact():
    tar_path = "/home/user/artifact.tar.gz"
    assert os.path.isfile(tar_path), f"Tarball {tar_path} is missing."

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(path=tmpdir)
        except tarfile.TarError as e:
            pytest.fail(f"Failed to extract {tar_path}: {e}")

        artifact_dir = os.path.join(tmpdir, "artifact")
        assert os.path.isdir(artifact_dir), "The tarball does not contain an 'artifact/' directory at its root."

        yield artifact_dir

def test_metrics_json(extracted_artifact):
    metrics_path = os.path.join(extracted_artifact, "metrics.json")
    assert os.path.isfile(metrics_path), "metrics.json is missing from the artifact directory."

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("metrics.json is not valid JSON.")

    assert "mse" in metrics, "metrics.json does not contain the 'mse' key."
    mse = metrics["mse"]
    assert isinstance(mse, (int, float)), "'mse' value must be a number."
    assert 0.0 < mse < 2.0, f"MSE value {mse} is outside the expected reasonable bounds based on the true noise variance."

def test_weights_txt(extracted_artifact):
    weights_path = os.path.join(extracted_artifact, "weights.txt")
    assert os.path.isfile(weights_path), "weights.txt is missing from the artifact directory."

    with open(weights_path, "r") as f:
        weights_str = f.read().strip()

    parts = weights_str.split(",")
    assert len(parts) == 2, "weights.txt should contain exactly two comma-separated values."

    try:
        w1 = float(parts[0])
        w2 = float(parts[1])
    except ValueError:
        pytest.fail("The values in weights.txt are not valid floats.")

    # The true weights are approximately 3.5 and -2.1
    assert 2.5 < w1 < 4.5, f"First weight {w1} is outside expected bounds (should be around 3.5)."
    assert -3.5 < w2 < -1.0, f"Second weight {w2} is outside expected bounds (should be around -2.1)."