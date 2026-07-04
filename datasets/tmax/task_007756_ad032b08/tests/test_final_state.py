# test_final_state.py

import os
import pytest

def test_z_layers_output():
    output_file = "/home/user/z_layers.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip().splitlines()

    expected = [
        "0.200",
        "0.400",
        "0.600",
        "0.800",
        "1.000",
        "1.200"
    ]

    assert content == expected, f"Content of {output_file} does not match expected output. Got: {content}"

def test_no_gcode_file_on_disk():
    # The task explicitly states not to extract the .gcode file to disk.
    assert not os.path.exists("/home/user/machine.gcode"), "/home/user/machine.gcode was extracted to disk, but it should have been streamed."
    assert not os.path.exists("/home/user/archive/machine.gcode"), "machine.gcode was found in the archive directory."

def test_python_script_exists():
    script_file = "/home/user/parse_gcode.py"
    assert os.path.isfile(script_file), f"Python script {script_file} does not exist."