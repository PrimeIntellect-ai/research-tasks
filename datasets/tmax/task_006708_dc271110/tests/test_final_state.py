# test_final_state.py
import os
import subprocess
import pytest

def test_main_rs_recovered():
    """Verify that the deleted main.rs file has been recovered."""
    assert os.path.isfile("/home/user/data_pipeline/src/main.rs"), (
        "The file /home/user/data_pipeline/src/main.rs has not been recovered."
    )

def test_cargo_builds():
    """Verify that the Rust project compiles successfully (compiler error fixed)."""
    # We expect the file to exist first
    assert os.path.isfile("/home/user/data_pipeline/src/main.rs"), "main.rs is missing."

    result = subprocess.run(
        ["cargo", "build"],
        cwd="/home/user/data_pipeline",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, (
        f"Cargo build failed. The recovered code may still have compiler errors.\n"
        f"Stderr:\n{result.stderr}"
    )

def test_anomaly_txt_content():
    """Verify that the anomaly value was correctly identified and written to the report file."""
    anomaly_path = "/home/user/anomaly.txt"
    assert os.path.isfile(anomaly_path), f"The report file {anomaly_path} does not exist."

    with open(anomaly_path, "r") as f:
        content = f.read().strip()

    assert content == "5000.5", (
        f"The anomaly value in {anomaly_path} is incorrect. "
        f"Expected '5000.5', got '{content}'."
    )