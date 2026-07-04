# test_final_state.py

import os
import re
import pytest

def test_solution_file_exists():
    assert os.path.isfile("/home/user/solution.txt"), "The file /home/user/solution.txt does not exist."

def test_solution_file_content():
    with open("/home/user/solution.txt", "r") as f:
        content = f.read().strip().split('\n')

    assert len(content) == 2, "The solution.txt file must contain exactly two lines."

    flag_line = content[0].strip()
    id_line = content[1].strip()

    assert flag_line == "Flag: -lm", f"Expected 'Flag: -lm', but got '{flag_line}'"
    assert id_line == "Bottleneck ID: 84", f"Expected 'Bottleneck ID: 84', but got '{id_line}'"

def test_build_script_fixed():
    assert os.path.isfile("/home/user/perf_test/build.sh"), "build.sh is missing."
    with open("/home/user/perf_test/build.sh", "r") as f:
        content = f.read()
    assert "-lm" in content, "The build.sh script does not contain the required '-lm' flag."

def test_cruncher_binary_exists():
    assert os.path.isfile("/home/user/perf_test/cruncher"), "The cruncher binary was not built."
    assert os.access("/home/user/perf_test/cruncher", os.X_OK), "The cruncher binary is not executable."