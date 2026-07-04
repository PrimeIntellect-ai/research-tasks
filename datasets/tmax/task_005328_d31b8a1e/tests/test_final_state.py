# test_final_state.py

import os
import sys
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"

def test_module_import_and_functionality():
    """Test if data_processor is built, can be imported, and works correctly."""
    # Add project dir to sys.path in case it was built in-place or installed in env
    sys.path.insert(0, PROJECT_DIR)

    try:
        import data_processor
    except ImportError:
        pytest.fail("Failed to import 'data_processor'. Ensure the extension was built successfully.")

    assert hasattr(data_processor, "process_data"), "Module 'data_processor' lacks 'process_data' function."

    # Test the functionality
    input_data = [3, 1, 2, 3, 4, 1, 5]
    expected_output = sorted(list(set(input_data)))

    try:
        actual_output = data_processor.process_data(input_data)
    except Exception as e:
        pytest.fail(f"data_processor.process_data raised an exception: {e}")

    assert actual_output == expected_output, f"Expected {expected_output}, got {actual_output}"

def test_prop_script():
    """Test if test_prop.py exists, uses hypothesis, and runs successfully."""
    script_path = os.path.join(PROJECT_DIR, "test_prop.py")
    assert os.path.isfile(script_path), f"Script not found: {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    assert "hypothesis" in content, "test_prop.py does not seem to use the 'hypothesis' library."

    # Run the script
    result = subprocess.run([sys.executable, script_path], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"test_prop.py failed with exit code {result.returncode}.\nStdout: {result.stdout}\nStderr: {result.stderr}"

def test_benchmark_json():
    """Test if benchmark.json exists and has the correct format."""
    json_path = os.path.join(PROJECT_DIR, "benchmark.json")
    assert os.path.isfile(json_path), f"Benchmark result not found: {json_path}"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("benchmark.json is not valid JSON.")

    assert "avg_time_sec" in data, "benchmark.json does not contain the key 'avg_time_sec'."
    assert isinstance(data["avg_time_sec"], (int, float)), "'avg_time_sec' must be a number."

def test_memory_txt():
    """Test if memory.txt exists and contains an integer."""
    mem_path = os.path.join(PROJECT_DIR, "memory.txt")
    assert os.path.isfile(mem_path), f"Memory result not found: {mem_path}"

    with open(mem_path, "r") as f:
        content = f.read().strip()

    try:
        mem_usage = int(content)
    except ValueError:
        pytest.fail(f"memory.txt does not contain a valid integer. Found: {content}")

    assert mem_usage >= 0, "Memory usage should be a non-negative integer."