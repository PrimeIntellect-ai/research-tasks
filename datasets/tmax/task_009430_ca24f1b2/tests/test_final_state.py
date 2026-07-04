# test_final_state.py
import os

def test_root_result_correct():
    result_path = "/home/user/optimization/root_result.txt"
    assert os.path.isfile(result_path), "root_result.txt was not generated."

    with open(result_path, "r") as f:
        content = f.read().strip()

    assert content == "-1.76929", f"Expected root to be '-1.76929', but got '{content}'."

def test_helper_py_fixed():
    helper_path = "/home/user/optimization/helper.py"
    assert os.path.isfile(helper_path), "helper.py is missing."

    with open(helper_path, "r") as f:
        lines = f.readlines()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("import obsolete_math_lib_v1"):
            assert False, "The broken import 'import obsolete_math_lib_v1' is still present and uncommented in helper.py."

def test_find_root_py_fixed():
    find_root_path = "/home/user/optimization/find_root.py"
    assert os.path.isfile(find_root_path), "find_root.py is missing."

    with open(find_root_path, "r") as f:
        content = f.read()

    assert re_search_x0(content), "The initial guess x0 = 0.0 was not changed in find_root.py."

def re_search_x0(content):
    # Just checking if x0 = 0.0 is still there
    # If it is, the user didn't change it.
    for line in content.splitlines():
        if line.strip() == "x0 = 0.0":
            return False
    return True