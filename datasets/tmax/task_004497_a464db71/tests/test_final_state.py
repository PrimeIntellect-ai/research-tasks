# test_final_state.py

import os

def test_builder_script_exists():
    assert os.path.isfile("/home/user/workspace/builder.py"), "builder.py is missing in /home/user/workspace/"

def test_run_test_script_exists():
    assert os.path.isfile("/home/user/workspace/run_test.py"), "run_test.py is missing in /home/user/workspace/"

def test_shared_libraries_exist():
    libraries = ["modA.so", "modB.so", "modC.so", "modD.so"]
    for lib in libraries:
        path = f"/home/user/workspace/{lib}"
        assert os.path.isfile(path), f"Compiled library {path} is missing. Ensure builder.py compiles the C files."

def test_result_txt_content():
    path = "/home/user/workspace/result.txt"
    assert os.path.isfile(path), "result.txt is missing in /home/user/workspace/"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content == "70", f"Expected result.txt to contain '70', but found '{content}'."