# test_final_state.py

import os
import subprocess
import numpy as np
import pytest

def test_pipeline_execution_and_mse():
    script_path = "/home/user/pipeline.sh"
    output_path = "/home/user/top10.txt"
    csv_path = "/home/user/profiles.csv"
    embedder_path = "/app/user_embedder"

    # Check script exists and is executable
    assert os.path.exists(script_path), f"Script {script_path} not found."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Execute the pipeline script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStderr: {result.stderr}"

    # Check output file exists
    assert os.path.exists(output_path), f"Output file {output_path} not found."

    # Generate ground-truth embeddings
    with open(csv_path, "r") as f:
        lines = f.readlines()

    cleaned_lines = []
    for line in lines:
        parts = line.strip().split(",")
        # Replace empty values with 0.0
        cleaned_parts = [p if p != "" else "0.0" for p in parts]
        cleaned_lines.append(" ".join(cleaned_parts))

    cleaned_input = "\n".join(cleaned_lines) + "\n"

    embed_result = subprocess.run([embedder_path], input=cleaned_input, capture_output=True, text=True)
    assert embed_result.returncode == 0, f"Failed to run embedder for truth generation. Stderr: {embed_result.stderr}"

    embeddings = []
    for line in embed_result.stdout.strip().split("\n"):
        if line.strip():
            embeddings.append([float(x) for x in line.strip().split()])
    embeddings = np.array(embeddings)

    # Read the output and compute MSE
    predicted_distances = []
    true_distances = []

    with open(output_path, "r") as f:
        out_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(out_lines) == 10, f"Expected exactly 10 lines in {output_path}, but got {len(out_lines)}."

    for line in out_lines:
        parts = line.split()
        assert len(parts) == 3, f"Invalid line format in {output_path}: '{line}'. Expected 'RowA RowB Distance'."

        try:
            row_a = int(parts[0])
            row_b = int(parts[1])
            dist = float(parts[2])
        except ValueError:
            pytest.fail(f"Could not parse numeric values from line: '{line}'")

        assert row_a < row_b, f"RowA should be less than RowB, got {row_a} and {row_b}."
        assert 1 <= row_a <= len(embeddings), f"RowA {row_a} is out of bounds."
        assert 1 <= row_b <= len(embeddings), f"RowB {row_b} is out of bounds."

        idx_a = row_a - 1
        idx_b = row_b - 1

        true_dist = np.linalg.norm(embeddings[idx_a] - embeddings[idx_b])

        predicted_distances.append(dist)
        true_distances.append(true_dist)

    predicted_distances = np.array(predicted_distances)
    true_distances = np.array(true_distances)

    mse = np.mean((predicted_distances - true_distances) ** 2)
    threshold = 1e-4

    assert mse <= threshold, f"Calculated MSE {mse:.6e} exceeds the threshold of {threshold}. Predicted distances might be incorrect."