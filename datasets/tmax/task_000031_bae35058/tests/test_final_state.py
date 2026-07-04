# test_final_state.py

import os
import json
import subprocess
import pytest

def test_failed_files_json():
    json_path = "/home/user/diagnostics/failed_files.json"
    assert os.path.isfile(json_path), f"The file {json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert isinstance(data, list), f"The JSON in {json_path} must be an array."

    expected_files = {
        "/data/inputs/financial summary final.pdf",
        "/data/inputs/user backups/archive.tar.gz"
    }

    actual_files = set(data)
    assert actual_files == expected_files, (
        f"The extracted failed files do not match the expected list.\n"
        f"Expected: {expected_files}\n"
        f"Found: {actual_files}"
    )

def test_processor_rs_fixed():
    processor_rs = "/home/user/rusty-dispatcher/src/processor.rs"
    assert os.path.isfile(processor_rs), f"{processor_rs} does not exist."

    with open(processor_rs, "r") as f:
        content = f.read()

    # The bug should be fixed, meaning it shouldn't use `sh -c` with concatenated strings
    assert "Command::new(\"sh\")" not in content, "The code still uses Command::new(\"sh\"), which is unsafe for this use case."
    assert "arg(\"-c\")" not in content, "The code still passes '-c' to a shell, indicating the bug might not be properly fixed."

def test_regression_test_exists():
    processor_rs = "/home/user/rusty-dispatcher/src/processor.rs"
    assert os.path.isfile(processor_rs), f"{processor_rs} does not exist."

    with open(processor_rs, "r") as f:
        content = f.read()

    assert "test_filename_with_spaces_regression" in content, (
        "The regression test `test_filename_with_spaces_regression` was not found in processor.rs."
    )

def test_cargo_test_passes():
    project_dir = "/home/user/rusty-dispatcher"
    assert os.path.isdir(project_dir), f"Project directory {project_dir} does not exist."

    # Run cargo test
    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, (
        f"`cargo test` failed in {project_dir}.\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )