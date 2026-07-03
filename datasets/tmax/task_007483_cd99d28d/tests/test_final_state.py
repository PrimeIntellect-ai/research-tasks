# test_final_state.py

import os
import json
import subprocess
import pytest

def test_circular_dependency_removed():
    module_b_path = "/home/user/app/lib/module_b.sh"
    assert os.path.exists(module_b_path), f"{module_b_path} is missing."
    with open(module_b_path, "r") as f:
        content = f.read()
    assert "source /home/user/app/lib/module_a.sh" not in content, \
        "The circular dependency 'source /home/user/app/lib/module_a.sh' is still present in module_b.sh."

def test_shared_library_linkage_fixed():
    lib_path = "/home/user/app/lib/libsemver.so.1"
    assert os.path.exists(lib_path), \
        f"Shared library symlink {lib_path} is missing. The binary vercheck requires this to run."

    # Test if vercheck can run successfully now
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = "/home/user/app/lib:" + env.get("LD_LIBRARY_PATH", "")
    try:
        result = subprocess.run(
            ["/home/user/app/bin/vercheck", "1.0.0"],
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        assert "VALID" in result.stdout, "vercheck did not return expected output when executed."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"vercheck failed to execute properly: {e.stderr}")

def test_processed_data_generated_and_correct():
    output_file = "/home/user/processed_data.json"
    assert os.path.exists(output_file), \
        f"The output file {output_file} was not generated. Did you run /home/user/app/run.sh?"

    with open(output_file, "r") as f:
        content = f.read()

    try:
        data = json.loads(content)
    except json.JSONDecodeError as e:
        pytest.fail(f"The file {output_file} does not contain valid JSON. Error: {e}")

    expected_data = [
        {"app": "nginx", "version": "1.21.0"},
        {"app": "redis", "version": "6.2.5"},
        {"app": "python", "version": "3.9.7"}
    ]

    assert isinstance(data, list), "The JSON output should be a list of objects."
    assert len(data) == len(expected_data), f"Expected {len(expected_data)} items, found {len(data)}."

    for expected_item in expected_data:
        assert expected_item in data, f"Expected item {expected_item} not found in the processed data."