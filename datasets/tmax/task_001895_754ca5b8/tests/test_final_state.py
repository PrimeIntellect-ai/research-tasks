# test_final_state.py

import os
import json
import pytest

def test_binary_exists_and_executable():
    binary_path = "/home/user/deploy_api/target/x86_64-unknown-linux-musl/release/deploy_api"
    assert os.path.exists(binary_path), f"The musl release binary was not found at {binary_path}."
    assert os.path.isfile(binary_path), f"The path {binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"The binary at {binary_path} is not executable."

def test_json_output_exists_and_correct():
    json_path = "/home/user/deployment_deps.json"
    assert os.path.exists(json_path), f"The output JSON file was not found at {json_path}."
    assert os.path.isfile(json_path), f"The path {json_path} is not a file."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_data = {
        "merged": ["4.0.0", "3.0.1", "2.1.0", "1.2.3", "1.0.0"]
    }

    assert data == expected_data, f"The JSON output does not match the expected result. Got: {data}"

def test_main_rs_fixed():
    main_rs_path = "/home/user/deploy_api/src/main.rs"
    assert os.path.exists(main_rs_path), f"The source file {main_rs_path} is missing."

    with open(main_rs_path, "r") as f:
        content = f.read()

    # The original error was `l1.push(*item);`
    # It should have been fixed, so this exact string should likely be gone or changed.
    # We won't strictly enforce how it was fixed (e.g., clone() or extend()), 
    # but we can verify the file is readable and exists.
    assert "axum" in content, "The axum framework usage seems to have been removed from src/main.rs."