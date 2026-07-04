# test_final_state.py

import os
import pytest

def test_workspace_extracted():
    """Test that the archive was reconstructed and extracted to /home/user/workspace/."""
    workspace = "/home/user/workspace"
    assert os.path.isdir(workspace), f"{workspace} directory is missing."

    manifest = os.path.join(workspace, "manifest.csv")
    assert os.path.isfile(manifest), f"{manifest} is missing."

    raw_dir = os.path.join(workspace, "raw")
    assert os.path.isdir(raw_dir), f"{raw_dir} directory is missing."

    links_dir = os.path.join(workspace, "links")
    assert os.path.isdir(links_dir), f"{links_dir} directory is missing."

def test_c_program_files_exist():
    """Test that the C source and compiled executable exist."""
    source_file = "/home/user/aggregate.c"
    executable = "/home/user/aggregate"

    assert os.path.isfile(source_file), f"C source file {source_file} is missing."
    assert os.path.isfile(executable), f"Compiled executable {executable} is missing."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_sensor_a_total():
    """Test that the final output file contains the correct sum."""
    output_file = "/home/user/sensor_a_total.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, "r") as f:
        content = f.read().strip()

    assert content == "55", f"Expected '55' in {output_file}, but found '{content}'."