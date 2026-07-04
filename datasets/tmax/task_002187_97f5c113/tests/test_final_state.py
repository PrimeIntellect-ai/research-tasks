# test_final_state.py
import os
import sys
import glob
import pytest

def test_success_log_exists_and_correct():
    log_path = "/home/user/success.log"
    assert os.path.exists(log_path), f"File {log_path} does not exist. Did you create it?"

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "BUILD SUCCESS", f"Expected '{log_path}' to contain 'BUILD SUCCESS', but got '{content}'."

def test_extension_built_inplace():
    project_dir = "/home/user/mathparser_mobile"
    assert os.path.exists(project_dir), f"Directory {project_dir} is missing."

    # Check for the built extension (e.g., mathparser.cpython-310-x86_64-linux-gnu.so)
    so_files = glob.glob(os.path.join(project_dir, "mathparser*.so"))
    assert len(so_files) > 0, "No compiled C extension (.so file) found in the project directory. Did you build with --inplace?"

def test_mathparser_functionality():
    project_dir = "/home/user/mathparser_mobile"

    # Ensure the project directory is in the python path to import the in-place built module
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)

    try:
        import mathparser
    except ImportError as e:
        pytest.fail(f"Failed to import 'mathparser'. Is the C extension built correctly? Error: {e}")

    # Evaluate 2.0 and 3.0: (2+3)^2 + (2*3) = 25 + 6 = 31.0
    try:
        result = mathparser.evaluate(2.0, 3.0)
    except Exception as e:
        pytest.fail(f"Calling mathparser.evaluate(2.0, 3.0) raised an exception: {e}")

    expected = 31.0
    assert abs(result - expected) < 1e-6, f"mathparser.evaluate(2.0, 3.0) returned {result}, expected {expected}. Did the math library get linked properly?"