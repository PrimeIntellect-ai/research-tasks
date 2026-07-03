# test_final_state.py

import os
import re

PROJECT_DIR = "/home/user/project"

def test_libcalc_c_fixed():
    file_path = os.path.join(PROJECT_DIR, "libcalc.c")
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    # The bug was `i <= len`. It should be fixed to `i < len` or similar logic.
    assert "i <= len" not in content, "The memory safety bug (i <= len) is still present in libcalc.c."
    assert "i < len" in content or "i<len" in content or "i!=len" in content, "libcalc.c does not seem to have the corrected loop bounds."

def test_setup_py_fixed():
    file_path = os.path.join(PROJECT_DIR, "setup.py")
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    assert "libcalc.c" in content, "setup.py was not updated to include 'libcalc.c' in the sources list."

def test_test_calc_py_has_property_based_tests():
    file_path = os.path.join(PROJECT_DIR, "test_calc.py")
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read()

    assert "@given" in content, "test_calc.py does not contain the '@given' decorator for hypothesis tests."
    assert "hypothesis" in content, "test_calc.py does not seem to import hypothesis."

def test_test_log_txt_passed():
    file_path = os.path.join(PROJECT_DIR, "test_log.txt")
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Tests might not have been run or output not captured."

    with open(file_path, "r") as f:
        content = f.read()

    # Pytest output usually ends with something like "1 passed in 0.12s"
    assert re.search(r"\b1 passed\b", content), "test_log.txt does not indicate that exactly 1 test passed."

def test_extension_built():
    # Check if the compiled extension exists (.so file)
    files = os.listdir(PROJECT_DIR)
    so_files = [f for f in files if f.startswith("calc_ext") and f.endswith(".so")]
    assert len(so_files) > 0, "The C-extension was not built in-place (no .so file found in the project directory)."