# test_final_state.py

import os
import re

def test_release_report_exists():
    """Check if the release_report.txt file is created."""
    report_path = "/home/user/release_prep/release_report.txt"
    assert os.path.isfile(report_path), f"{report_path} does not exist."

def test_release_report_content():
    """Verify the contents of the release report."""
    report_path = "/home/user/release_prep/release_report.txt"
    with open(report_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Report: Release Candidate 1 has hash: 798" in content, "Rust validator output is missing or incorrect in the report."
    assert "Integral: 8.6667" in content, "Simpson's rule output is missing or incorrect in the report."
    assert "Cumsum: 15.0" in content, "Cumulative sum output is missing or incorrect in the report."

def test_c_shared_library_exists():
    """Check if the compiled C shared library exists."""
    lib_path = "/home/user/release_prep/c_src/libmath.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not compiled."

def test_rust_executable_exists():
    """Check if the compiled Rust executable exists."""
    exe_path = "/home/user/release_prep/rust_src/validator"
    assert os.path.isfile(exe_path), f"Rust executable {exe_path} was not compiled."
    assert os.access(exe_path, os.X_OK), f"Rust executable {exe_path} is not executable."

def test_c_source_fixed():
    """Check if the C source code was fixed (i < n instead of i <= n)."""
    c_src_path = "/home/user/release_prep/c_src/math_core.c"
    assert os.path.isfile(c_src_path), f"{c_src_path} is missing."
    with open(c_src_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The bug was `i <= n`, it should be `i < n`.
    assert re.search(r"i\s*<\s*n", content) is not None, "The buffer overflow bug in math_core.c (i <= n) was not fixed."

def test_build_script_exists():
    """Check if the build script exists and is executable."""
    script_path = "/home/user/release_prep/build_release.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    with open(script_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "-DRELEASE_MODE=1" in content, "The build script does not include the -DRELEASE_MODE=1 flag for gcc."