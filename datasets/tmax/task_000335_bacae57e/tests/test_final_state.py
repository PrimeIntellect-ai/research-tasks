# test_final_state.py

import os
import subprocess
import re
import pytest

PROJECT_DIR = "/home/user/forensic_project"
REPORT_PATH = "/home/user/debug_report.txt"

def test_makefile_builds_successfully():
    """Ensure that the project builds successfully using the fixed Makefile."""
    # Run make clean then make
    subprocess.run(["make", "clean"], cwd=PROJECT_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    result = subprocess.run(["make"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"make failed with error:\n{result.stderr}"

    # Check if the executable exists
    exe_path = os.path.join(PROJECT_DIR, "forensic_tool")
    assert os.path.isfile(exe_path), "forensic_tool executable was not created by make."

def test_auth_h_signature_fixed():
    """Check if auth.h has the correct signature for generate_token."""
    auth_h_path = os.path.join(PROJECT_DIR, "include", "auth.h")
    assert os.path.isfile(auth_h_path), "include/auth.h is missing."

    with open(auth_h_path, "r") as f:
        content = f.read()

    # Looking for void generate_token(int, char*, int)
    # Parameter names might vary, so we just check the types loosely
    match = re.search(r"void\s+generate_token\s*\(\s*int\b[^,]*,\s*char\s*\*\b[^,]*,\s*int\b[^)]*\)\s*;", content)
    assert match is not None, "auth.h does not contain the correct signature for generate_token."

def test_extractor_c_uses_strtok_r():
    """Check if extractor.c was updated to use the thread-safe strtok_r."""
    extractor_path = os.path.join(PROJECT_DIR, "extractor.c")
    assert os.path.isfile(extractor_path), "extractor.c is missing."

    with open(extractor_path, "r") as f:
        content = f.read()

    assert "strtok_r" in content, "extractor.c does not use the thread-safe strtok_r function."
    assert re.search(r"\bstrtok\s*\(", content) is None, "extractor.c still contains calls to the non-thread-safe strtok."

def test_regression_test_exists_and_passes():
    """Check if regression_test.c exists, compiles, and passes."""
    reg_src = os.path.join(PROJECT_DIR, "regression_test.c")
    assert os.path.isfile(reg_src), "regression_test.c is missing."

    reg_exe = os.path.join(PROJECT_DIR, "regression_test")
    assert os.path.isfile(reg_exe), "regression_test executable is missing. Make sure it is compiled."

    # Run the regression test
    # Need to make sure LD_LIBRARY_PATH includes ./lib if it uses libauth, though it might just link extractor.o
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = os.path.join(PROJECT_DIR, "lib") + ":" + env.get("LD_LIBRARY_PATH", "")

    result = subprocess.run([reg_exe], cwd=PROJECT_DIR, capture_output=True, env=env)
    assert result.returncode == 0, "regression_test failed (non-zero exit code)."

def test_debug_report_contents():
    """Check if debug_report.txt exists and contains the required information."""
    assert os.path.isfile(REPORT_PATH), "debug_report.txt is missing."

    with open(REPORT_PATH, "r") as f:
        content = f.read()

    assert re.search(r"THREAD_SAFE_FUNC:\s*strtok_r", content), "debug_report.txt missing or incorrect THREAD_SAFE_FUNC."
    assert re.search(r"REGRESSION_PASS:\s*YES", content), "debug_report.txt missing or incorrect REGRESSION_PASS."

    # Check signature roughly
    assert re.search(r"SIGNATURE:\s*void\s+generate_token", content), "debug_report.txt missing or incorrect SIGNATURE."