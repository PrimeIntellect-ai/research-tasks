# test_final_state.py
import os
import json
import re

def test_result_json_exists_and_valid():
    """Verify that result.json is generated and contains the correct execution results."""
    result_path = "/home/user/result.json"
    assert os.path.exists(result_path), f"Expected output file {result_path} does not exist. Did you run `cargo run --release`?"

    with open(result_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{result_path} does not contain valid JSON."

    assert "vendor" in data, "JSON missing 'vendor' field."
    assert "semver_check" in data, "JSON missing 'semver_check' field."
    assert "bench_success" in data, "JSON missing 'bench_success' field."

    assert data["semver_check"] is True, "semver_check is not true. The semver logic failed."
    assert data["bench_success"] is True, "bench_success is not true. Benchmarking failed."

    vendor = data["vendor"]
    assert isinstance(vendor, str), "vendor field is not a string."
    assert len(vendor) == 12, f"vendor string should be exactly 12 characters, got {len(vendor)} ('{vendor}')."
    assert vendor != "\x00" * 12, "vendor string is all null bytes. The cpuid_vendor function was not correctly implemented."

def test_cargo_toml_updated():
    """Verify that Cargo.toml was updated to a 1.x version of semver."""
    cargo_toml_path = "/home/user/min_tool/Cargo.toml"
    assert os.path.exists(cargo_toml_path), f"{cargo_toml_path} is missing."

    with open(cargo_toml_path, "r") as f:
        content = f.read()

    # Check that semver is updated to 1.x. The code won't compile without it, 
    # but we sanity check the file to ensure the student made the change.
    assert "semver" in content, "semver dependency is missing from Cargo.toml"
    assert "0.9.0" not in content, "Cargo.toml still contains the old 0.9.0 semver dependency."