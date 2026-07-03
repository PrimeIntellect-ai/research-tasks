# test_final_state.py
import os
import subprocess
import pytest

def test_cargo_test_passes():
    """Verify that the cargo test suite passes after the fix."""
    project_dir = "/home/user/kepler_solver"
    assert os.path.isdir(project_dir), f"Directory {project_dir} does not exist."

    result = subprocess.run(
        ["cargo", "test", "--quiet"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed with output:\n{result.stdout}\n{result.stderr}"

def test_debugging_summary_contents():
    """Verify the contents of the debugging_summary.txt file."""
    summary_file = "/home/user/debugging_summary.txt"
    assert os.path.isfile(summary_file), f"Summary file {summary_file} does not exist."

    with open(summary_file, 'r') as f:
        lines = [line.strip() for line in f.read().splitlines() if line.strip() != ""]

    assert len(lines) >= 3, f"Expected at least 3 non-empty lines in {summary_file}, found {len(lines)}."

    expected_line_1 = "let derivative = 1.0 + e * e_curr.cos();"
    expected_line_2 = "let derivative = 1.0 - e * e_curr.cos();"
    expected_line_3 = "ALL TESTS PASSED"

    assert lines[0] == expected_line_1, f"Line 1 mismatch. Expected: '{expected_line_1}', Got: '{lines[0]}'"
    assert lines[1] == expected_line_2, f"Line 2 mismatch. Expected: '{expected_line_2}', Got: '{lines[1]}'"
    assert lines[2] == expected_line_3, f"Line 3 mismatch. Expected: '{expected_line_3}', Got: '{lines[2]}'"

def test_lib_rs_is_fixed():
    """Verify that the bug in src/lib.rs has actually been fixed."""
    lib_rs = "/home/user/kepler_solver/src/lib.rs"
    assert os.path.isfile(lib_rs), f"File {lib_rs} does not exist."

    with open(lib_rs, 'r') as f:
        content = f.read()

    assert "let derivative = 1.0 - e * e_curr.cos();" in content, "The correct derivative formula was not found in src/lib.rs."
    assert "let derivative = 1.0 + e * e_curr.cos();" not in content, "The old buggy derivative formula is still present in src/lib.rs."