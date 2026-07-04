# test_final_state.py
import os
import pytest

PIPELINE_DIR = "/home/user/pipeline"
C_FILE = os.path.join(PIPELINE_DIR, "fast_counter.c")
SETUP_FILE = os.path.join(PIPELINE_DIR, "setup.py")
OUTPUT_FILE = os.path.join(PIPELINE_DIR, "output.log")
VENV_DIR = "/home/user/venv"

def test_c_file_updated_for_python3():
    assert os.path.isfile(C_FILE), f"File {C_FILE} does not exist."
    with open(C_FILE, "r") as f:
        content = f.read()

    # Check that legacy Python 2 API calls are removed
    assert "PyInt_FromLong" not in content, "Legacy PyInt_FromLong is still in fast_counter.c"
    assert "Py_InitModule" not in content, "Legacy Py_InitModule is still in fast_counter.c"

    # Check that Python 3 API calls are present
    assert "PyLong_FromLong" in content, "fast_counter.c does not use PyLong_FromLong"
    assert "PyModuleDef" in content, "fast_counter.c does not define a PyModuleDef struct"
    assert "PyInit_word_counter" in content, "fast_counter.c does not have PyInit_word_counter initialization function"

def test_setup_py_exists():
    assert os.path.isfile(SETUP_FILE), f"File {SETUP_FILE} does not exist. You need to create it to build the extension."

def test_venv_exists():
    assert os.path.isdir(VENV_DIR), f"Virtual environment directory {VENV_DIR} does not exist."
    python_bin = os.path.join(VENV_DIR, "bin", "python")
    assert os.path.isfile(python_bin), f"Python executable not found in virtual environment at {python_bin}."

def test_output_log_correct():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist. Did you run process.py and redirect the output?"
    with open(OUTPUT_FILE, "r") as f:
        content = f.read().strip()

    expected = "Migration successful! Total words processed: 15"
    assert expected in content, f"Output log does not contain the expected success message. Found: {content}"