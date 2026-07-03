# test_final_state.py

import os
import pytest

def test_libgraph_so_exists():
    """Verify that the shared library libgraph.so was compiled."""
    lib_path = "/home/user/workspace/libgraph.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} was not found. Did you compile graph.c?"

def test_resolve_py_exists_and_uses_ctypes():
    """Verify that resolve.py exists and imports ctypes."""
    script_path = "/home/user/workspace/resolve.py"
    assert os.path.isfile(script_path), f"Python script {script_path} was not found."

    with open(script_path, "r") as f:
        content = f.read()

    assert "ctypes" in content, "resolve.py does not appear to use the ctypes module."
    assert "get_build_order" in content, "resolve.py does not appear to call get_build_order."
    assert "free_build_order" in content, "resolve.py does not appear to call free_build_order."

def test_build_order_output():
    """Verify that build_order.txt contains the correct topological sort."""
    output_path = "/home/user/workspace/build_order.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_order = [
        "module_e",
        "module_d",
        "module_b",
        "module_c",
        "module_a",
        "module_f"
    ]

    assert lines == expected_order, f"build_order.txt content is incorrect. Expected {expected_order}, got {lines}."

def test_graph_c_bugs_fixed():
    """Verify that graph.c no longer contains the specific memory bugs."""
    c_path = "/home/user/workspace/graph.c"
    assert os.path.isfile(c_path), f"Source file {c_path} is missing."

    with open(c_path, "r") as f:
        content = f.read()

    # Bug 1: Missing +1 in malloc
    assert "malloc(strlen(name));" not in content, "Bug 1 (missing +1 for null terminator in malloc) is still present in graph.c."

    # Bug 2: Returning stack-allocated array
    # The original code had `char* result[100];`. It should be dynamically allocated.
    assert "char* result[100];" not in content, "Bug 2 (stack-allocated result array) is still present in graph.c."