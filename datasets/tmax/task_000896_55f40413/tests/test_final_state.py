# test_final_state.py

import os
import pytest

def test_resolutions_file_exists():
    resolutions_path = "/home/user/resolutions.txt"
    assert os.path.exists(resolutions_path), f"Missing required file: {resolutions_path}"
    assert os.path.isfile(resolutions_path), f"Path is not a file: {resolutions_path}"

def test_resolutions_content():
    resolutions_path = "/home/user/resolutions.txt"
    assert os.path.exists(resolutions_path), f"Missing required file: {resolutions_path}"

    with open(resolutions_path, "r") as f:
        content = f.read().strip()

    assert content, "resolutions.txt is empty"

    # Parse the file content into a dictionary
    blocks = content.split("\n\n")
    parsed_resolutions = {}
    for block in blocks:
        lines = [line.strip() for line in block.split("\n") if line.strip()]
        if not lines:
            continue
        header = lines[0]
        assert header.startswith("[") and header.endswith("]"), f"Invalid header format: {header}"
        target = header[1:-1]
        parsed_resolutions[target] = lines[1:]

    expected_resolutions = {
        "app_alpha@1.0.0": [
            "app_alpha@1.0.0",
            "lib_core@1.2.0",
            "lib_crypto@1.0.0",
            "lib_net@2.0.0",
            "lib_utils@2.1.0"
        ],
        "app_beta@2.1.0": [
            "app_beta@2.1.0",
            "lib_auth@2.0.0",
            "lib_core@2.0.0",
            "lib_crypto@2.1.0",
            "lib_utils@2.1.0"
        ],
        "app_gamma@3.0.0": [
            "app_gamma@3.0.0",
            "lib_core@1.2.0",
            "lib_crypto@1.0.0",
            "lib_utils@2.1.0"
        ]
    }

    # Verify each target and its exact dependencies
    for target, expected_deps in expected_resolutions.items():
        assert target in parsed_resolutions, f"Target '{target}' is missing from resolutions.txt"
        actual_deps = parsed_resolutions[target]
        assert actual_deps == expected_deps, (
            f"Dependencies for '{target}' do not match expected.\n"
            f"Expected: {expected_deps}\n"
            f"Got:      {actual_deps}"
        )

    # Check for extra targets that shouldn't be there
    for target in parsed_resolutions:
        assert target in expected_resolutions, f"Unexpected target '{target}' found in resolutions.txt"