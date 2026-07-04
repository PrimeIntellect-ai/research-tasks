# test_final_state.py
import os
import json
import subprocess
import pytest

def test_parsed_metrics_json():
    path = "/home/user/parsed_metrics.json"
    assert os.path.exists(path), f"Missing output file: {path}"

    with open(path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {path} does not contain valid JSON.")

    expected = [
        {"type": "battery", "value": 42},
        {"type": "device", "value": "PIXEL"}
    ]

    assert isinstance(data, list), "Parsed JSON should be an array."
    assert len(data) == 2, f"Expected 2 parsed metrics, got {len(data)}."
    assert data == expected, f"JSON content does not match expected valid packets. Got: {data}"

def test_c_code_fixed():
    path = "/home/user/mobile_telemetry/src/legacy_decoder.c"
    assert os.path.exists(path), f"Missing C file: {path}"

    with open(path, "r") as f:
        content = f.read()

    # The bug was unconditionally adding 3 to in_idx. A bounds check must involve the length.
    has_bounds_check = ("in_len" in content) and (
        "3" in content and ("<" in content or ">" in content or "==" in content)
    )
    assert has_bounds_check, "The C code does not appear to have a bounds check for the 0xFF skip marker."

def test_rust_code_arch_function():
    path = "/home/user/mobile_telemetry/src/main.rs"
    assert os.path.exists(path), f"Missing Rust main file: {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "get_pipeline_arch" in content, "Missing get_pipeline_arch function in main.rs"
    assert "aarch64" in content, "Function does not seem to return 'aarch64'"
    assert "x86_64" in content, "Function does not seem to return 'x86_64'"

    # Check for some form of conditional compilation (either #[cfg(...)] or cfg!(...))
    assert "cfg" in content and "target_arch" in content, "Missing conditional compilation logic for target architecture."

def test_cross_compilation():
    project_dir = "/home/user/mobile_telemetry"
    assert os.path.exists(project_dir), f"Missing project directory: {project_dir}"

    result = subprocess.run(
        ["cargo", "build", "--target", "aarch64-unknown-linux-gnu"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Cross-compilation for aarch64 failed.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"