# test_final_state.py

import os
import re
import pytest

def test_rust_project_configuration():
    cargo_toml_path = "/home/user/decoder/Cargo.toml"
    assert os.path.isfile(cargo_toml_path), f"Cargo.toml missing at {cargo_toml_path}"

    with open(cargo_toml_path, "r") as f:
        content = f.read()

    # Check for cdylib configuration
    assert "cdylib" in content, "Cargo.toml does not specify crate-type as 'cdylib'"

def test_rust_library_compiled():
    so_path = "/home/user/decoder/target/release/libdecoder.so"
    assert os.path.isfile(so_path), f"Compiled Rust library not found at {so_path}. Did you build in release mode?"

def test_python_script_exists():
    script_path = "/home/user/app/process.py"
    assert os.path.isfile(script_path), f"Python script missing at {script_path}"

def test_decoded_output():
    output_path = "/home/user/app/decoded.txt"
    assert os.path.isfile(output_path), f"Decoded output file missing at {output_path}"

    with open(output_path, "r", encoding="utf-8") as f:
        content = f.read().strip()

    expected_text = "Secret Rust FFI Migration Payload 2024!"
    assert content == expected_text, f"Decoded text does not match the expected payload. Got: {content}"

def test_migration_patch():
    patch_path = "/home/user/app/migration.patch"
    assert os.path.isfile(patch_path), f"Migration patch missing at {patch_path}"

    with open(patch_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    assert len(lines) >= 2, "Patch file is too short"

    # Check for unified diff headers
    has_minus = any(line.startswith("--- ") for line in lines[:5])
    has_plus = any(line.startswith("+++ ") for line in lines[:5])

    assert has_minus and has_plus, "Patch file does not appear to be a valid unified diff (missing --- or +++ headers)"

    content = "".join(lines)
    assert "legacy_process.py" in content, "Patch file does not reference legacy_process.py"
    assert "process.py" in content, "Patch file does not reference process.py"