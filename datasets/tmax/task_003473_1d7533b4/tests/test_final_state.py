# test_final_state.py

import os
import pytest

def test_solve_linking_script_exists():
    script_path = "/home/user/solve_linking.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist. Did you create it?"

def test_link_order_file_exists():
    output_path = "/home/user/link_order.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist. Did you run your script?"

def test_link_order_contents():
    output_path = "/home/user/link_order.txt"
    if not os.path.exists(output_path):
        pytest.fail(f"Cannot check contents because {output_path} is missing.")

    expected_order = [
        "libMain",
        "libMatrix",
        "libVector",
        "libMath",
        "libIO",
        "libCore"
    ]

    with open(output_path, "r") as f:
        # Read lines, strip whitespace, and ignore empty lines
        actual_order = [line.strip() for line in f.readlines() if line.strip()]

    assert actual_order == expected_order, (
        f"The linking order in {output_path} is incorrect.\n"
        f"Expected: {expected_order}\n"
        f"Actual:   {actual_order}"
    )