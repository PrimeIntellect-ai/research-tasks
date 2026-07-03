# test_final_state.py

import os
import shutil
import subprocess
import tempfile
import pytest

def test_filter_data_executable_exists():
    executable_path = "/home/user/filter_data"
    assert os.path.exists(executable_path), f"Executable {executable_path} does not exist."
    assert os.path.isfile(executable_path), f"{executable_path} is not a file."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_filter_data_correctness():
    clean_dir = "/verify/clean"
    evil_dir = "/verify/evil"

    assert os.path.exists(clean_dir), f"Missing clean corpus dir: {clean_dir}"
    assert os.path.exists(evil_dir), f"Missing evil corpus dir: {evil_dir}"

    clean_files = set(os.listdir(clean_dir))
    evil_files = set(os.listdir(evil_dir))

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    with tempfile.TemporaryDirectory() as input_dir, tempfile.TemporaryDirectory() as output_dir:
        # Mix clean and evil files into the input directory
        for f in clean_files:
            shutil.copy(os.path.join(clean_dir, f), os.path.join(input_dir, f))
        for f in evil_files:
            shutil.copy(os.path.join(evil_dir, f), os.path.join(input_dir, f))

        # Run the agent's executable
        executable_path = "/home/user/filter_data"
        try:
            result = subprocess.run(
                [executable_path, input_dir, output_dir],
                capture_output=True,
                text=True,
                timeout=60
            )
        except subprocess.TimeoutExpired:
            pytest.fail("Execution of /home/user/filter_data timed out after 60 seconds.")

        assert result.returncode == 0, f"Executable failed with return code {result.returncode}.\nStderr: {result.stderr}"

        # Check output directory
        output_files = set(os.listdir(output_dir))

        clean_preserved = clean_files.intersection(output_files)
        clean_modified = clean_files - output_files

        evil_bypassed = evil_files.intersection(output_files)
        evil_rejected = evil_files - output_files

        errors = []
        if clean_modified:
            errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified/rejected (e.g., {list(clean_modified)[:5]})")
        if evil_bypassed:
            errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed (e.g., {list(evil_bypassed)[:5]})")

        if errors:
            pytest.fail(" | ".join(errors))