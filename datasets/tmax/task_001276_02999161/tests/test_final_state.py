# test_final_state.py
import os
import glob
import pytest

WORKSPACE_DIR = "/home/user/rate_limiter"

def test_setup_py_fixed():
    setup_path = os.path.join(WORKSPACE_DIR, "setup.py")
    assert os.path.isfile(setup_path), f"Missing {setup_path}"

    with open(setup_path, "r") as f:
        content = f.read()

    assert "_bucket" in content, "setup.py does not define the extension name as '_bucket'"
    assert "bucket.c" in content, "setup.py does not include 'bucket.c' in sources"

def test_extension_built():
    so_files = glob.glob(os.path.join(WORKSPACE_DIR, "_bucket*.so"))
    assert len(so_files) > 0, "The C-extension module _bucket*.so was not found in the workspace. Did you build it in-place?"

def test_test_limiter_py_content():
    test_path = os.path.join(WORKSPACE_DIR, "test_limiter.py")
    assert os.path.isfile(test_path), f"Missing {test_path}"

    with open(test_path, "r") as f:
        content = f.read()

    required_strings = [
        "hypothesis",
        "given",
        "st.lists",
        "st.integers",
        "TokenBucket",
        "consume",
        "get_tokens",
        "100",
        "0"
    ]

    for req in required_strings:
        assert req in content, f"Expected to find '{req}' in test_limiter.py"

def test_report_log_passed():
    log_path = os.path.join(WORKSPACE_DIR, "test_report.log")
    assert os.path.isfile(log_path), f"Missing {log_path}"

    with open(log_path, "r") as f:
        content = f.read()

    assert "1 passed" in content, "test_report.log does not indicate that 1 test passed."