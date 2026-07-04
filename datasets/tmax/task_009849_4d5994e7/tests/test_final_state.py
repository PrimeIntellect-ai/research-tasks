# test_final_state.py
import os

def test_math_ops_cpp_fixed():
    cpp_file = "/home/user/math_api/src/math_ops.cpp"
    assert os.path.isfile(cpp_file), f"File {cpp_file} does not exist."
    with open(cpp_file, "r") as f:
        content = f.read()
    assert 'extern "C"' in content, "math_ops.cpp does not contain 'extern \"C\"' to fix the ABI."

def test_app_py_fixed():
    app_file = "/home/user/math_api/api/app.py"
    assert os.path.isfile(app_file), f"File {app_file} does not exist."
    with open(app_file, "r") as f:
        content = f.read()
    assert "<float:a>" in content and "<float:b>" in content, "app.py does not contain <float:a> and <float:b> in the route."

def test_shared_library_built():
    lib_file = "/home/user/math_api/build/libmath_ops.so"
    assert os.path.isfile(lib_file), f"Shared library {lib_file} was not built."

def test_test_results_file():
    results_file = "/home/user/test_results.txt"
    assert os.path.isfile(results_file), f"File {results_file} does not exist."
    with open(results_file, "r") as f:
        content = f.read()
    assert "1 passed" in content or "passed in" in content or "100%" in content, "test_results.txt does not indicate a successful pytest run."