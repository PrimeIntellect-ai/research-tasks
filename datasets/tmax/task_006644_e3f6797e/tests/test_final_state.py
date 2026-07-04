# test_final_state.py

import os
import json
import subprocess
import pytest

def test_resolution_json_exists_and_valid():
    path = "/home/user/resolution.json"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{path} is not a valid JSON file.")

    assert "recovered_api_key" in data, f"Key 'recovered_api_key' missing in {path}."
    assert "failing_endpoint_id" in data, f"Key 'failing_endpoint_id' missing in {path}."

    assert data["recovered_api_key"] == "sre-sec-99x1a2b3c", f"Incorrect recovered_api_key in {path}."
    assert data["failing_endpoint_id"] == "ep-0143", f"Incorrect failing_endpoint_id in {path}."

def test_rust_code_compiles():
    path = "/home/user/uptime-monitor"
    result = subprocess.run(
        ["cargo", "build"],
        cwd=path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo build failed:\n{result.stderr}"

def test_rust_code_runs_without_panic():
    path = "/home/user/uptime-monitor"
    result = subprocess.run(
        ["cargo", "run", "--", "process", "endpoints.json"],
        cwd=path,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo run failed or panicked:\n{result.stderr}\n{result.stdout}"
    assert "thread 'main' panicked" not in result.stderr, "Rust application panicked during execution."