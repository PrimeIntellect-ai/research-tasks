# test_final_state.py

import os
import re

PROJECT_DIR = "/home/user/legacy_project"
LOG_FILE = "/home/user/migration_result.log"

def test_setup_py_exists():
    setup_path = os.path.join(PROJECT_DIR, "setup.py")
    assert os.path.isfile(setup_path), f"setup.py does not exist at {setup_path}."

def test_migration_result_log():
    assert os.path.isfile(LOG_FILE), f"Log file {LOG_FILE} does not exist."
    with open(LOG_FILE, 'r') as f:
        content = f.read().strip()
    assert content == "Computed Metric: 5.5", f"Expected log content to be 'Computed Metric: 5.5', but got '{content}'."

def test_fastcalc_c_fixed():
    c_file = os.path.join(PROJECT_DIR, "fastcalc.c")
    assert os.path.isfile(c_file), f"{c_file} does not exist."

    with open(c_file, 'r') as f:
        content = f.read()

    # Check Python 3 initialization
    assert "Py_InitModule" not in content, "fastcalc.c still contains deprecated Py_InitModule."
    assert "PyModuleDef" in content, "fastcalc.c must contain PyModuleDef for Python 3 initialization."

    # Check memory safety fixes
    assert "i <= size" not in content, "fastcalc.c still contains the off-by-one bug (i <= size)."
    assert "i < size" in content, "fastcalc.c should use 'i < size' for the loop bounds."
    assert "free(" in content, "fastcalc.c must free the allocated memory to prevent memory leaks."

def test_process_py_fixed():
    py_file = os.path.join(PROJECT_DIR, "process.py")
    assert os.path.isfile(py_file), f"{py_file} does not exist."

    with open(py_file, 'r') as f:
        content = f.read()

    assert "xrange" not in content, "process.py still contains 'xrange' which is Python 2 specific."
    assert "range" in content, "process.py should use 'range' instead of 'xrange'."

    # Check for print function vs statement
    assert re.search(r'print\s*\(', content), "process.py must use the Python 3 print() function."