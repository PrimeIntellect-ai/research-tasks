# test_final_state.py

import os
import subprocess
import json
import pytest

def test_makefile_exists():
    """Check if the Makefile was created."""
    assert os.path.isfile("/home/user/Makefile"), "Makefile is missing in /home/user."

def test_scripts_exist():
    """Check if the required Python scripts exist."""
    assert os.path.isfile("/home/user/scripts/aggregate.py"), "/home/user/scripts/aggregate.py is missing."
    assert os.path.isfile("/home/user/scripts/pca_plot.py"), "/home/user/scripts/pca_plot.py is missing."

def test_make_clean_and_all():
    """Test the Makefile clean and all targets."""
    # Ensure Makefile exists before running
    if not os.path.isfile("/home/user/Makefile"):
        pytest.fail("Makefile is missing, cannot test targets.")

    # Test make clean
    result_clean = subprocess.run(
        ["make", "clean"],
        cwd="/home/user",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result_clean.returncode == 0, f"'make clean' failed: {result_clean.stderr.decode()}"

    # Verify files are removed
    assert not os.path.exists("/home/user/dataset/aggregated.csv"), "'make clean' did not remove aggregated.csv"
    assert not os.path.exists("/home/user/results/pca_plot.png"), "'make clean' did not remove pca_plot.png"
    assert not os.path.exists("/home/user/results/metrics.json"), "'make clean' did not remove metrics.json"

    # Test make (default target 'all')
    result_all = subprocess.run(
        ["make"],
        cwd="/home/user",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert result_all.returncode == 0, f"'make' failed: {result_all.stderr.decode()}"

def test_aggregated_csv_output():
    """Check if aggregated.csv is generated correctly after make."""
    file_path = "/home/user/dataset/aggregated.csv"
    assert os.path.isfile(file_path), f"{file_path} was not generated."

    with open(file_path, "r") as f:
        lines = f.readlines()

    # 5 unique sensor types + 1 header = 6 lines
    assert len(lines) == 6, f"Expected 6 lines in {file_path}, but found {len(lines)}."

    header = lines[0].strip().split(",")
    assert "sensor_type" in header, "'sensor_type' column missing in aggregated.csv"
    for i in range(1, 21):
        assert f"reading_{i}" in header or f"reading_{i}" in lines[0], f"'reading_{i}' missing in aggregated.csv header."

def test_pca_plot_output():
    """Check if pca_plot.png is generated and is a valid image file."""
    file_path = "/home/user/results/pca_plot.png"
    assert os.path.isfile(file_path), f"{file_path} was not generated."

    size = os.path.getsize(file_path)
    assert size > 100, f"{file_path} is too small ({size} bytes), likely an empty or corrupted image."

def test_metrics_json_output():
    """Check if metrics.json is generated and contains the correct structure."""
    file_path = "/home/user/results/metrics.json"
    assert os.path.isfile(file_path), f"{file_path} was not generated."

    with open(file_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{file_path} does not contain valid JSON.")

    assert "explained_variance_sum" in metrics, "Key 'explained_variance_sum' missing in metrics.json."
    assert isinstance(metrics["explained_variance_sum"], float), "'explained_variance_sum' must be a float."
    assert 0.0 <= metrics["explained_variance_sum"] <= 1.0, "'explained_variance_sum' should be between 0.0 and 1.0."