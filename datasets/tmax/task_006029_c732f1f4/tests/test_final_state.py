# test_final_state.py

import os
import json
import glob
import pytest

def test_constants_h_generated():
    json_path = '/home/user/polymath/data/matrix.json'
    header_path = '/home/user/polymath/src/constants.h'

    assert os.path.isfile(json_path), f"Expected JSON file at {json_path} is missing."
    assert os.path.isfile(header_path), f"Expected header file at {header_path} is missing. Did the script generate it?"

    with open(json_path, 'r') as f:
        data = json.load(f)

    with open(header_path, 'r') as f:
        header_content = f.read()

    for key, value in data.items():
        expected_macro = f"#define {key} {value}"
        assert expected_macro in header_content, f"Expected macro '{expected_macro}' not found in {header_path}."

def test_setup_py_fixed():
    setup_path = '/home/user/polymath/setup.py'
    assert os.path.isfile(setup_path), f"File {setup_path} is missing."

    with open(setup_path, 'r') as f:
        content = f.read()

    assert 'fib_ext' in content, "setup.py does not define the extension module 'fib_ext'."
    assert 'fib.c' in content, "setup.py does not reference the source file 'fib.c'."

def test_wheel_built():
    dist_dir = '/home/user/polymath/dist'
    assert os.path.isdir(dist_dir), f"Distribution directory {dist_dir} is missing. Was the wheel built?"

    wheels = glob.glob(os.path.join(dist_dir, '*.whl'))
    assert len(wheels) > 0, f"No wheel (.whl) files found in {dist_dir}. The build step may have failed."

def test_ci_result_txt():
    result_path = '/home/user/polymath/ci_result.txt'
    assert os.path.isfile(result_path), f"File {result_path} is missing. Did ci_build.sh execute successfully?"

    with open(result_path, 'r') as f:
        content = f.read()

    assert content == "55\n", f"Expected ci_result.txt to contain exactly '55\\n', but got {repr(content)}."

def test_fib_ext_installed():
    try:
        import fib_ext
        assert fib_ext.fib(10) == 55, "fib_ext.fib(10) did not return the expected value (55)."
    except ImportError:
        pytest.fail("Failed to import fib_ext. The wheel may not have been installed successfully.")