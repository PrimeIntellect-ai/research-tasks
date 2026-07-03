# test_final_state.py
import os
import subprocess

def test_pipeline_execution_and_artifacts():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Execute the pipeline script
    result = subprocess.run(
        [script_path, "--max_features", "50", "--c_value", "0.5"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"run_pipeline.sh failed with return code {result.returncode}. Stderr: {result.stderr}"

    # Verify experiments.csv
    exp_csv_path = "/home/user/experiments.csv"
    assert os.path.isfile(exp_csv_path), f"{exp_csv_path} was not created."

    with open(exp_csv_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) >= 2, f"{exp_csv_path} does not contain enough data (header + at least one row)."
    assert lines[0] == "id,max_features,C,accuracy", f"Header in {exp_csv_path} is incorrect. Got: {lines[0]}"

    # Verify the last row appended by our test run
    last_row = lines[-1].split(",")
    assert len(last_row) == 4, f"Expected 4 columns in the last row of {exp_csv_path}, got {len(last_row)}."

    exp_id, max_features, c_value, accuracy = last_row
    assert max_features == "50", f"Expected max_features to be 50, got {max_features}."
    assert c_value == "0.5", f"Expected C to be 0.5, got {c_value}."

    try:
        float(accuracy)
    except ValueError:
        assert False, f"Expected accuracy to be a float, got '{accuracy}'."

    # Verify artifact directory and files
    artifact_dir = f"/home/user/artifacts/exp_{exp_id}"
    assert os.path.isdir(artifact_dir), f"Artifact directory {artifact_dir} does not exist."

    model_path = os.path.join(artifact_dir, "model.pkl")
    processed_path = os.path.join(artifact_dir, "processed.csv")

    assert os.path.isfile(model_path), f"model.pkl is missing in {artifact_dir}."
    assert os.path.isfile(processed_path), f"processed.csv is missing in {artifact_dir}."

    # Verify preprocessing (lowercased and punctuation removed)
    with open(processed_path, "r") as f:
        processed_content = f.read()

    assert not any(c.isupper() for c in processed_content), "processed.csv contains uppercase characters, which should have been lowercased."

    for char in processed_content:
        # Allow alphanumeric, spaces, newlines, and commas
        if not (char.isalnum() or char in " \n,"):
            assert False, f"Found unexpected punctuation character '{char}' in processed.csv."