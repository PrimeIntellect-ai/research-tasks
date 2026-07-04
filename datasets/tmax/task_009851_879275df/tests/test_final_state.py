# test_final_state.py

import os
import sys
import stat
import subprocess
import pytest

try:
    import tomllib
except ImportError:
    pass # Fallback for older python, though 3.11+ is standard in these environments

def test_ring_buffer_implementation():
    ring_buffer_path = "/home/user/polybuild/src/polybuild/ring_buffer.py"
    assert os.path.isfile(ring_buffer_path), f"File {ring_buffer_path} does not exist."

    # Dynamically import the module
    sys.path.insert(0, "/home/user/polybuild/src")
    try:
        from polybuild.ring_buffer import RingBuffer
    except ImportError as e:
        pytest.fail(f"Failed to import RingBuffer from polybuild.ring_buffer: {e}")

    # Test the RingBuffer logic
    rb = RingBuffer(2)

    # Test empty pop
    with pytest.raises(IndexError) as excinfo:
        rb.pop()
    assert "empty" in str(excinfo.value).lower(), "Expected IndexError with 'empty' message when popping from empty buffer."

    # Test push and overwrite
    rb.push(1)
    rb.push(2)
    rb.push(3) # Overwrites 1

    val = rb.pop()
    assert val == 2, f"Expected 2, got {val}. The oldest element was not correctly overwritten or popped."

    val2 = rb.pop()
    assert val2 == 3, f"Expected 3, got {val2}."

    with pytest.raises(IndexError):
        rb.pop()

def test_pyproject_toml_fixed():
    toml_file = "/home/user/polybuild/pyproject.toml"
    assert os.path.isfile(toml_file), f"File {toml_file} does not exist."

    with open(toml_file, "rb") as f:
        if "tomllib" in sys.modules:
            data = tomllib.load(f)

            # Check build-system
            build_system = data.get("build-system", {})
            requires = build_system.get("requires", [])
            assert any("setuptools" in req.lower() for req in requires), "pyproject.toml missing setuptools in build-system.requires"

            backend = build_system.get("build-backend", "")
            assert "setuptools" in backend, "pyproject.toml build-backend should use setuptools"

            # Check project
            project = data.get("project", {})
            assert project.get("name") == "polybuild", f"Expected project name 'polybuild', got {project.get('name')}"
            assert project.get("version") == "0.1.0", f"Expected project version '0.1.0', got {project.get('version')}"
        else:
            # Fallback string matching if tomllib is not available
            content = f.read().decode("utf-8")
            assert "setuptools" in content, "pyproject.toml does not contain 'setuptools'"
            assert 'name = "polybuild"' in content.replace("'", '"'), "pyproject.toml does not contain correct name"
            assert 'version = "0.1.0"' in content.replace("'", '"'), "pyproject.toml does not contain correct version"

def test_ci_pipeline_execution():
    script_path = "/home/user/polybuild/ci_pipeline.sh"
    log_path = "/home/user/polybuild/ci_status.log"

    assert os.path.isfile(script_path), f"File {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert st.st_mode & stat.S_IXUSR, f"Script {script_path} is not executable."

    # Remove log if exists to ensure clean run
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run the script
    result = subprocess.run([script_path], cwd="/home/user/polybuild", capture_output=True, text=True)
    assert result.returncode == 0, f"ci_pipeline.sh failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

    # Check the log
    assert os.path.isfile(log_path), f"Log file {log_path} was not created by the script."
    with open(log_path, "r") as f:
        log_content = f.read().strip()

    expected_log = "CI_SUCCESS: polybuild pipeline passed"
    assert log_content == expected_log, f"Expected log content '{expected_log}', got '{log_content}'"