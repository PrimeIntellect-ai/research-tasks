# test_final_state.py

import os
import subprocess
import glob
import re
import pytest

def test_setup_py_fixed():
    setup_path = "/home/user/data_processor/setup.py"
    assert os.path.isfile(setup_path), f"Missing file: {setup_path}"
    with open(setup_path, "r") as f:
        content = f.read()
    assert "data_processor/fast_hash.c" in content, "setup.py was not updated to point to the correct C source file."

def test_c_extension_built():
    ext_dir = "/home/user/data_processor/data_processor"
    assert os.path.isdir(ext_dir), f"Directory not found: {ext_dir}"
    so_files = glob.glob(os.path.join(ext_dir, "fast_hash*.so"))
    assert len(so_files) > 0, "C-extension .so file not found in /home/user/data_processor/data_processor/. Did you build it in-place?"

def test_download_fixtures_script():
    script_path = "/home/user/data_processor/scripts/download_fixtures.sh"
    assert os.path.isfile(script_path), f"Missing file: {script_path}"

    # Run the script in its directory so it can create/check files correctly
    script_dir = os.path.dirname(script_path)
    result = subprocess.run(["bash", script_path], cwd=script_dir, capture_output=True, text=True)

    assert result.returncode == 0, f"Script failed with exit code {result.returncode}. Output: {result.stdout}\n{result.stderr}"

def test_utils_refactored():
    utils_path = "/home/user/data_processor/data_processor/utils.py"
    assert os.path.isfile(utils_path), f"Missing file: {utils_path}"
    with open(utils_path, "r") as f:
        content = f.read()

    assert "def get_mode" in content, "utils.py does not define a get_mode() function."
    assert "MODE =" not in content, "utils.py still contains the module-level MODE constant."

def test_test_processing_refactored():
    test_path = "/home/user/data_processor/tests/test_processing.py"
    assert os.path.isfile(test_path), f"Missing file: {test_path}"
    with open(test_path, "r") as f:
        content = f.read()

    assert "get_mode" in content, "test_processing.py does not call get_mode()."
    assert "pytest.fixture" in content or "fixture" in content, "test_processing.py does not use a pytest fixture as requested."

def test_test_results_log():
    log_path = "/home/user/test_results.txt"
    assert os.path.isfile(log_path), f"Missing file: {log_path}. Did you run pytest and save the output?"
    with open(log_path, "r") as f:
        content = f.read()

    # Check that tests passed (e.g., "2 passed" or "passed")
    assert re.search(r'\bpassed\b', content.lower()), "test_results.txt does not indicate that tests passed."
    assert "failed" not in content.lower() or "0 failed" in content.lower(), "test_results.txt indicates there are test failures."