# test_final_state.py

import os
import pytest

HEADER_FILE = "/home/user/build_config.h"

def test_build_config_exists():
    assert os.path.isfile(HEADER_FILE), f"Missing generated header file: {HEADER_FILE}"

def test_build_config_contents_and_sorting():
    with open(HEADER_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    defines = []
    for line in lines:
        parts = line.split()
        assert len(parts) >= 3, f"Invalid line format in {HEADER_FILE}: '{line}'"
        assert parts[0] == "#define", f"Line does not start with #define: '{line}'"
        var_name = parts[1]
        try:
            value = int(parts[2])
        except ValueError:
            pytest.fail(f"Value for {var_name} is not an integer: '{parts[2]}'")
        defines.append((var_name, value))

    # Check sorting
    var_names = [d[0] for d in defines]
    sorted_var_names = sorted(var_names)
    assert var_names == sorted_var_names, "The #define directives are not sorted alphabetically by variable name."

    # Check exact expected values
    expected_values = {
        "API_LEVEL": 33,
        "CPU_CORES": 8,
        "FEATURE_ADVANCED": 2,
        "FEATURE_CAMERA_X": 1,
        "FEATURE_HEAVY_PROCESSING": 1,
        "FEATURE_PRO_UI": 2,
        "FINAL_SCORE": 3,
        "HAS_MULTI_CORE": 1,
        "IS_PRO_BUILD": 1,
        "LEGACY_SUPPORT": 0,
        "MIN_API": 24,
        "RAM_MB": 4096,
    }

    actual_values = dict(defines)

    # Check all expected keys are present
    for key, expected_val in expected_values.items():
        assert key in actual_values, f"Missing variable in {HEADER_FILE}: {key}"
        assert actual_values[key] == expected_val, f"Incorrect value for {key}. Expected {expected_val}, got {actual_values[key]}"

    # Check no extra keys are present
    for key in actual_values:
        assert key in expected_values, f"Unexpected variable in {HEADER_FILE}: {key}"