# test_final_state.py
import os
import subprocess
import pytest

def test_analysis_result_exists():
    result_path = "/home/user/analysis_result.txt"
    assert os.path.isfile(result_path), f"The file {result_path} does not exist."

def test_analysis_result_content():
    result_path = "/home/user/analysis_result.txt"
    if not os.path.isfile(result_path):
        pytest.fail(f"Cannot check content because {result_path} is missing.")

    with open(result_path, "r") as f:
        content = f.read()

    assert "Anomaly detected at frame 423" in content, (
        f"Expected 'Anomaly detected at frame 423' in {result_path}, but it was not found."
    )

def test_rust_code_compiles_and_runs():
    project_dir = "/home/user/beacon_parser"
    payload_path = "/home/user/payload.bin"

    # Check if we can build
    build_proc = subprocess.run(
        ["cargo", "build"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert build_proc.returncode == 0, f"Cargo build failed:\n{build_proc.stderr}"

    # Check if we can run without panicking
    run_proc = subprocess.run(
        ["cargo", "run", "--", payload_path],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert run_proc.returncode == 0, f"Parser did not exit cleanly (code 0). Stderr:\n{run_proc.stderr}"
    assert "Anomaly detected at frame 423" in run_proc.stdout, (
        "The parser output did not contain the expected anomaly message when run on the payload."
    )