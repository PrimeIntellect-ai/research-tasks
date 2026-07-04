# test_final_state.py
import os
import subprocess
import pytest

def test_build_lookup_import_order():
    file_path = "/home/user/mobile_pipeline/build_lookup.py"
    assert os.path.isfile(file_path), f"{file_path} is missing"

    with open(file_path, "r") as f:
        content = f.read()

    # Check that mobile_emulator is imported before math.sin is imported or used
    idx_emulator = content.find("import mobile_emulator")
    idx_sin = content.find("from math import sin")
    if idx_sin == -1:
        idx_sin = content.find("import math")

    assert idx_emulator != -1, "build_lookup.py is missing 'import mobile_emulator'"
    assert idx_sin != -1, "build_lookup.py is missing math import"

    assert idx_emulator < idx_sin, "In build_lookup.py, 'import mobile_emulator' must appear before math is imported to correctly patch it."

def test_lookup_arm64_header_exists_and_correct():
    header_path = "/home/user/mobile_pipeline/lookup_arm64.h"
    assert os.path.isfile(header_path), f"{header_path} was not generated. Did you run build_lookup.py with TARGET_ARCH=arm64?"

    with open(header_path, "r") as f:
        content = f.read()

    # Check for some rounded values to ensure it was patched
    assert "0.39f," in content or "0.39" in content, "The generated header does not contain the correctly patched (rounded) values."
    assert "0.48f," in content or "0.48" in content, "The generated header does not contain the correctly patched (rounded) values."

def test_test_lookup_passes():
    env = os.environ.copy()
    env["TARGET_ARCH"] = "arm64"
    env["PYTHONPATH"] = "/home/user/mobile_pipeline"

    result = subprocess.run(
        ["python3", "/home/user/mobile_pipeline/test_lookup.py"],
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"test_lookup.py failed with output:\n{result.stdout}\n{result.stderr}"
    assert "PASS" in result.stdout, "test_lookup.py did not output PASS."