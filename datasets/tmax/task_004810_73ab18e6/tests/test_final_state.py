# test_final_state.py

import os
import subprocess
import pytest

def test_diagnostic_file_correct():
    diagnostic_path = "/home/user/diagnostic.txt"
    assert os.path.isfile(diagnostic_path), f"The diagnostic file {diagnostic_path} is missing."

    with open(diagnostic_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    expected_lines = [
        "File: simulation.cpp",
        "Function: step2",
        "Line: 8"
    ]

    assert len(lines) == 3, f"Expected exactly 3 lines in diagnostic.txt, found {len(lines)}."

    for i, expected in enumerate(expected_lines):
        assert lines[i] == expected, f"Line {i+1} in diagnostic.txt is incorrect. Expected '{expected}', got '{lines[i]}'."

def test_simulation_fixed_and_recompiled():
    exe_path = "/home/user/sim/sim_run"
    assert os.path.isfile(exe_path), f"The executable {exe_path} is missing. Did you recompile?"

    result = subprocess.run([exe_path], capture_output=True, text=True)
    assert result.returncode == 0, f"sim_run failed with return code {result.returncode}"

    output = result.stdout.strip()
    expected_output = "3.141592653589793"

    assert output == expected_output, f"Expected the simulation to output '{expected_output}', but got '{output}'. The precision bug is not fixed correctly or the code wasn't recompiled."

def test_source_code_fixed():
    src_path = "/home/user/sim/simulation.cpp"
    assert os.path.isfile(src_path), f"The source file {src_path} is missing."

    with open(src_path, "r") as f:
        content = f.read()

    # The original buggy line was `float temp = val;`
    # We should ensure that precision loss is avoided, meaning `float` is no longer used for `temp`
    assert "float temp" not in content, "The source code still contains 'float temp', which causes precision loss."