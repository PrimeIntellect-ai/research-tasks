# test_final_state.py

import os
import json
import pytest

def test_benchmark_script_exists():
    """Verify that the benchmark script was created."""
    script_path = "/home/user/benchmark.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_metrics_json_exists_and_valid():
    """Verify that metrics.json exists, is valid JSON, and contains correct values."""
    metrics_path = "/home/user/results/metrics.json"
    assert os.path.isfile(metrics_path), f"The file {metrics_path} does not exist."

    with open(metrics_path, "r") as f:
        try:
            metrics = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {metrics_path} does not contain valid JSON.")

    assert "total_tokens" in metrics, "Missing 'total_tokens' in metrics.json"
    assert "time_seconds" in metrics, "Missing 'time_seconds' in metrics.json"

    # Check total_tokens
    assert isinstance(metrics["total_tokens"], int), "'total_tokens' must be an integer."
    assert metrics["total_tokens"] == 93, f"Expected 93 total tokens, got {metrics['total_tokens']}."

    # Check time_seconds
    assert isinstance(metrics["time_seconds"], (int, float)), "'time_seconds' must be a number."
    assert metrics["time_seconds"] > 0, "'time_seconds' must be a positive float."

def test_token_dist_png_exists_and_valid():
    """Verify that token_dist.png exists and is a valid PNG image."""
    png_path = "/home/user/results/token_dist.png"
    assert os.path.isfile(png_path), f"The file {png_path} does not exist."

    with open(png_path, "rb") as f:
        header = f.read(8)

    png_magic = b"\x89PNG\r\n\x1a\n"
    assert header == png_magic, f"The file {png_path} is not a valid PNG image."