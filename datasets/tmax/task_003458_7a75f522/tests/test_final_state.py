# test_final_state.py

import os
import re

def test_diagnostics_file_correct():
    diag_path = "/home/user/diagnostics.txt"
    assert os.path.isfile(diag_path), f"The file {diag_path} does not exist. Did you save the output?"

    with open(diag_path, "r") as f:
        content = f.read().strip()

    assert "Average: 3750000.25" in content, (
        f"Incorrect average in {diag_path}. "
        f"Expected 'Average: 3750000.25', but got:\n{content}\n"
        "Check if you properly skipped malformed lines and used f64 for precision."
    )

def test_main_rs_uses_f64():
    main_path = "/home/user/telemetry_app/src/main.rs"
    assert os.path.isfile(main_path), f"The file {main_path} does not exist."

    with open(main_path, "r") as f:
        content = f.read()

    assert "f64" in content, (
        "The source code does not appear to use 'f64'. "
        "You must upgrade the math logic to use 64-bit precision."
    )