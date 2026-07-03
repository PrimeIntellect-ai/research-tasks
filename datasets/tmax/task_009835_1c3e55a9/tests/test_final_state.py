# test_final_state.py

import os
import json
import subprocess
import shutil

CARGO_TOML_PATH = "/home/user/bcd_eval/Cargo.toml"
BCD_CONFIG_PATH = "/home/user/build_config.bcd"
JSON_OUTPUT_PATH = "/home/user/mobile_mock.json"

def test_rust_project_exists():
    """Ensure the Rust project was created at the correct path."""
    assert os.path.isfile(CARGO_TOML_PATH), f"Rust project Cargo.toml not found at {CARGO_TOML_PATH}"

def test_cargo_run_success_and_json_output():
    """Run the Rust program with the original config and verify the JSON output."""
    # Ensure we start fresh
    if os.path.exists(JSON_OUTPUT_PATH):
        os.remove(JSON_OUTPUT_PATH)

    # Run the program
    result = subprocess.run(
        ["cargo", "run", "--manifest-path", CARGO_TOML_PATH],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"cargo run failed with exit code {result.returncode}. stderr: {result.stderr}"
    assert os.path.isfile(JSON_OUTPUT_PATH), f"Expected output file {JSON_OUTPUT_PATH} was not created."

    with open(JSON_OUTPUT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {JSON_OUTPUT_PATH} does not contain valid JSON.")

    expected_data = {
        "ScreenWidth": 1080,
        "ScreenHeight": 1920,
        "Multiplier": 4,
        "Buffer": 512,
        "MaxMemory": 8294912,
        "ApiEndpoint": "/api/v2/config",
        "RateLimit": 45,
        "BurstThreshold": 100
    }

    assert data == expected_data, f"JSON output does not match expected values. Got: {data}"

def test_rate_limit_validation():
    """Modify the config to have RateLimit > 60 and verify the program exits with code 1."""
    # Backup original config
    backup_path = BCD_CONFIG_PATH + ".bak"
    shutil.copy(BCD_CONFIG_PATH, backup_path)

    try:
        # Modify config
        with open(BCD_CONFIG_PATH, "r") as f:
            content = f.read()

        content = content.replace("RateLimit = 45", "RateLimit = 65")

        with open(BCD_CONFIG_PATH, "w") as f:
            f.write(content)

        # Run the program
        result = subprocess.run(
            ["cargo", "run", "--manifest-path", CARGO_TOML_PATH],
            capture_output=True,
            text=True
        )

        assert result.returncode == 1, f"Expected exit code 1 when RateLimit > 60, but got {result.returncode}."

    finally:
        # Restore original config
        shutil.move(backup_path, BCD_CONFIG_PATH)