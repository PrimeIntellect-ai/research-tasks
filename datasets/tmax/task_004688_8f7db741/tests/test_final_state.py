# test_final_state.py

import os
import subprocess
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script not found at {script_path}"
    assert os.access(script_path, os.X_OK), f"Pipeline script at {script_path} is not executable"

def test_pipeline_execution_and_outputs():
    script_path = "/home/user/pipeline.sh"

    # Execute the pipeline script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed to execute. stderr: {result.stderr}"

    # 1. Check best_params.txt
    best_params_path = "/home/user/best_params.txt"
    assert os.path.isfile(best_params_path), f"{best_params_path} was not created"

    with open(best_params_path, "r") as f:
        best_params_content = f.read().strip()

    # Normalize spaces and check the exact string format expected
    normalized_content = " ".join(best_params_content.split())
    expected_content = "X=2.5, Y=3.5, Z=100.00"
    # Allow for slight variations like X=2.50 or missing commas, but check values
    assert "X=2.5" in normalized_content, f"Expected X=2.5 in {best_params_path}, got: {best_params_content}"
    assert "Y=3.5" in normalized_content, f"Expected Y=3.5 in {best_params_path}, got: {best_params_content}"
    assert "100.00" in normalized_content or "100" in normalized_content, f"Expected Z=100.00 in {best_params_path}, got: {best_params_content}"

    # 2. Check grid_data.txt
    grid_data_path = "/home/user/grid_data.txt"
    assert os.path.isfile(grid_data_path), f"{grid_data_path} was not created"

    with open(grid_data_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 11, f"Expected 11 rows in {grid_data_path}, found {len(lines)}"

    matrix = []
    for i, line in enumerate(lines):
        cols = line.split()
        assert len(cols) == 11, f"Expected 11 columns in row {i+1} of {grid_data_path}, found {len(cols)}"
        matrix.append([float(val) for val in cols])

    # Check specific values
    # Y=0.0, X=0.0 -> row 0, col 0
    val_0_0 = matrix[0][0]
    assert abs(val_0_0 - 81.50) < 0.01, f"Expected 81.50 at Y=0.0, X=0.0, got {val_0_0}"

    # Y=3.5, X=2.5 -> row 7, col 5
    val_opt = matrix[7][5]
    assert abs(val_opt - 100.00) < 0.01, f"Expected 100.00 at Y=3.5, X=2.5, got {val_opt}"

    # 3. Check plot.gp
    plot_gp_path = "/home/user/plot.gp"
    assert os.path.isfile(plot_gp_path), f"{plot_gp_path} was not created"
    with open(plot_gp_path, "r") as f:
        plot_content = f.read()
    assert "grid_data.txt" in plot_content, f"Expected 'grid_data.txt' to be referenced in {plot_gp_path}"
    assert "heatmap.png" in plot_content, f"Expected 'heatmap.png' to be referenced in {plot_gp_path}"

    # 4. Check heatmap.png
    heatmap_path = "/home/user/heatmap.png"
    assert os.path.isfile(heatmap_path), f"{heatmap_path} was not created"

    with open(heatmap_path, "rb") as f:
        header = f.read(8)

    png_signature = b'\x89PNG\r\n\x1a\n'
    assert header == png_signature, f"{heatmap_path} is not a valid PNG file"