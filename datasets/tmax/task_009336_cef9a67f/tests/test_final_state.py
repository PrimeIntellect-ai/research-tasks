# test_final_state.py
import os
import re
import pytest

def test_result_file():
    result_path = "/home/user/result.txt"
    assert os.path.isfile(result_path), f"File {result_path} is missing."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    # The expected format is: CI for A: [0.1234, 0.5678]
    pattern = r"^CI for A:\s*\[(0\.\d{4}),\s*(0\.\d{4})\]$"
    match = re.match(pattern, content)
    assert match is not None, f"File content '{content}' does not match expected format 'CI for A: [0.xxxx, 0.yyyy]'."

    lower_bound = float(match.group(1))
    upper_bound = float(match.group(2))

    expected_lower = 0.2311
    expected_upper = 0.2546
    tolerance = 0.005

    assert abs(lower_bound - expected_lower) <= tolerance, \
        f"Lower bound {lower_bound} is not within {tolerance} of expected {expected_lower}."
    assert abs(upper_bound - expected_upper) <= tolerance, \
        f"Upper bound {upper_bound} is not within {tolerance} of expected {expected_upper}."

def test_rust_project_exists():
    cargo_toml = "/home/user/markov_ci/Cargo.toml"
    assert os.path.isfile(cargo_toml), f"Rust project file {cargo_toml} is missing."

    with open(cargo_toml, 'r') as f:
        content = f.read()

    assert "rayon" in content, "Dependency 'rayon' missing in Cargo.toml"
    assert "rand" in content, "Dependency 'rand' missing in Cargo.toml"
    assert "nalgebra" in content, "Dependency 'nalgebra' missing in Cargo.toml"