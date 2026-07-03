# test_final_state.py

import os
import re
import stat

def test_run_sh_exists_and_executable():
    path = "/home/user/run.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {path} is not executable."

def test_test_xss_py_exists_and_content():
    path = "/home/user/test_xss.py"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "import ctypes" in content or "from ctypes import" in content, "ctypes module not imported in test_xss.py"
    assert "hypothesis" in content, "hypothesis module not imported in test_xss.py"
    assert "Payload" in content, "Payload struct not defined in test_xss.py"
    assert "@given" in content, "@given decorator not used in test_xss.py"

def test_shared_library_built():
    # run.sh is supposed to build this, so it should exist if the task was completed
    # However, since we are just checking the final state *after* the student has run their script (or we run it),
    # we assume the user has executed run.sh or the environment has.
    # The prompt says "The verification: 2. Run /home/user/run.sh." 
    # But usually, the test suite itself runs after the student's work. 
    # If the student didn't run it, we might need to run it, but typical tasks assume the student ran it or we just check the output.
    # Let's check if the file exists. If not, we can try running run.sh.
    so_path = "/home/user/url_parser/build/libxss_check.so"
    if not os.path.exists(so_path):
        # Try running the script to generate it
        os.system("/home/user/run.sh")

    assert os.path.isfile(so_path), f"Shared library {so_path} was not built."

def test_report_txt_valid():
    path = "/home/user/report.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "AssertionError" not in content, "report.txt contains AssertionError, indicating a test failure."
    assert "Traceback" not in content, "report.txt contains Traceback, indicating an error."