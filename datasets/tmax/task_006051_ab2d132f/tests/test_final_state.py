# test_final_state.py

import os
import json
import subprocess
import tempfile
import pytest

def test_interpreter_sh_exists_and_executable():
    interpreter_path = "/home/user/interpreter.sh"
    assert os.path.isfile(interpreter_path), f"{interpreter_path} is missing"
    assert os.access(interpreter_path, os.X_OK), f"{interpreter_path} is not executable"

def test_interpreter_sh_correctness():
    interpreter_path = "/home/user/interpreter.sh"
    # Create a small test DSL
    # "hello" base64 is "aGVsbG8="
    # "world" base64 is "d29ybGQ="
    # "helloworld" base64 is "aGVsbG93b3JsZA=="
    test_dsl = """PUSH aGVsbG8
PUSH 3b3JsZA==
CONCAT
B64DEC
PRINT
"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write(test_dsl)
        temp_path = f.name

    try:
        result = subprocess.run([interpreter_path, temp_path], capture_output=True, text=True)
        assert result.returncode == 0, f"Interpreter failed with return code {result.returncode}. Stderr: {result.stderr}"
        assert result.stdout == "helloworld", f"Interpreter output incorrect. Expected 'helloworld', got {repr(result.stdout)}"
    finally:
        os.remove(temp_path)

def test_metadata_json():
    metadata_path = "/home/user/metadata.json"
    assert os.path.isfile(metadata_path), f"{metadata_path} is missing"
    with open(metadata_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{metadata_path} does not contain valid JSON")

    assert data.get("version") == "1.2.3", f"Expected version '1.2.3' in metadata.json, got {data.get('version')}"
    assert data.get("deps") == ["requests"], f"Expected deps ['requests'] in metadata.json, got {data.get('deps')}"

def test_pyproject_toml_updated():
    toml_path = "/home/user/legacy_pkg/pyproject.toml"
    assert os.path.isfile(toml_path), f"{toml_path} is missing"

    with open(toml_path, "r") as f:
        content = f.read()

    # Check that placeholders are removed
    assert "# INSERT_VERSION_HERE" not in content, "Placeholder # INSERT_VERSION_HERE was not removed from pyproject.toml"
    assert "# INSERT_DEPS_HERE" not in content, "Placeholder # INSERT_DEPS_HERE was not removed from pyproject.toml"

    # Check for version and dependencies
    assert 'version = "1.2.3"' in content or "version='1.2.3'" in content.replace(" ", ""), "pyproject.toml missing correct version assignment"
    assert 'dependencies = ["requests"]' in content or "dependencies=['requests']" in content.replace(" ", ""), "pyproject.toml missing correct dependencies assignment"

def test_wheel_exists_in_artifacts():
    wheel_path = "/home/user/artifacts/legacy_pkg-1.2.3-py3-none-any.whl"
    assert os.path.isfile(wheel_path), f"Wheel file {wheel_path} is missing. Did you build the package and move it to artifacts?"