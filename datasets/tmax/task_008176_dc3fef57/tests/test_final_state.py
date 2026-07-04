# test_final_state.py

import os
import ast

def test_flag_file_exists():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"File {flag_path} does not exist. The pipeline was not successfully executed."

def test_flag_content():
    flag_path = "/home/user/flag.txt"
    assert os.path.isfile(flag_path), f"File {flag_path} is missing."

    # Recompute the expected flag from the AST structure in the truth data
    ast_repr = '["F", "L", "A", "G", "{", ["r", "3", "v", "3", "r", "s", "3"], "_", "3", "n", "g", "1", "n", "3", "3", "r", "}"]'
    ast_tree = ast.literal_eval(ast_repr)

    def evaluate(node):
        if isinstance(node, str):
            return node
        elif isinstance(node, list):
            return "".join([evaluate(item) for item in node])
        else:
            return ""

    expected_flag = evaluate(ast_tree)

    with open(flag_path, "r") as f:
        actual_flag = f.read().strip()

    assert actual_flag == expected_flag, f"The content of {flag_path} is incorrect. Expected '{expected_flag}', but got '{actual_flag}'."

def test_vm_script_fixed():
    vm_path = "/home/user/suspicious_repo/vm.py"
    assert os.path.isfile(vm_path), f"File {vm_path} is missing."

    with open(vm_path, "r") as f:
        content = f.read()

    # The original bug was `evaluate(node)` inside the list comprehension
    # A correct fix would use `evaluate(item)` or similar logic that doesn't pass the same `node` recursively
    assert "evaluate(item)" in content or "evaluate(node)" not in content, \
        "The infinite recursion bug in vm.py does not appear to be fixed."

def test_environment_misconfiguration_fixed():
    hashlib_path = "/home/user/suspicious_repo/lib/hashlib.py"
    # The misconfiguration can be fixed by removing the file or changing its content
    if os.path.isfile(hashlib_path):
        with open(hashlib_path, "r") as f:
            content = f.read()
        assert "raise ImportError" not in content, \
            "The environment misconfiguration in lib/hashlib.py is still present."