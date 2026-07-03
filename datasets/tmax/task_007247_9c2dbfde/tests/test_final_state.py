# test_final_state.py

import os
import json
import subprocess

def test_allocation_json_correctness():
    allocation_path = "/home/user/allocation.json"
    assert os.path.isfile(allocation_path), f"Missing output file: {allocation_path}"

    with open(allocation_path, "r") as f:
        try:
            allocation = json.load(f)
        except json.JSONDecodeError:
            assert False, "allocation.json is not a valid JSON file"

    expected_allocation = [
        ["file5.js", "file6.js"],
        ["file2.js", "file1.js", "file4.js"],
        ["file3.js"]
    ]

    assert allocation == expected_allocation, f"Allocation output does not match the expected deterministic bin packing. Got: {allocation}"

def test_cargo_test_passes():
    project_dir = "/home/user/organizer"
    assert os.path.isdir(project_dir), f"Missing project directory: {project_dir}"

    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"`cargo test` failed with output:\n{result.stdout}\n{result.stderr}"

def test_proptest_implemented():
    lib_rs_path = "/home/user/organizer/src/lib.rs"
    assert os.path.isfile(lib_rs_path), f"Missing lib.rs file: {lib_rs_path}"

    with open(lib_rs_path, "r") as f:
        content = f.read()

    assert "proptest!" in content or "proptest {" in content or "#[proptest]" in content, "No proptest macro found in lib.rs. You must implement a property-based test."