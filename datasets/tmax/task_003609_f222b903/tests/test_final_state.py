# test_final_state.py

import os
import json
import re

def test_process_py_fixed():
    path = "/home/user/project/process.py"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    assert "iteritems()" not in content, "process.py still contains Python 2 'iteritems()'."
    assert not re.search(r'print\s+"', content), "process.py still contains Python 2 print statements."
    assert "items()" in content, "process.py should use 'items()' instead of 'iteritems()'."
    assert "print(" in content, "process.py should use Python 3 'print()' function."

def test_myext_c_fixed():
    path = "/home/user/project/myext.c"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()

    # The original buggy code had exactly `malloc(len)`. It should be fixed to allocate at least len + 1.
    assert re.search(r'malloc\s*\(\s*len\s*\+\s*1\s*\)', content) or \
           re.search(r'calloc\s*\(', content) or \
           re.search(r'malloc\s*\(\s*len\s*\+\s*sizeof', content) or \
           re.search(r'malloc\s*\(\s*len\s*\+\s*2\s*\)', content), \
           "myext.c does not appear to have the malloc(len) bug fixed. Expected something like malloc(len + 1)."

def test_output_file():
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} was not created."

    graph_path = "/home/user/project/graph.json"
    assert os.path.isfile(graph_path), f"Graph file {graph_path} is missing."

    with open(graph_path, "r") as f:
        graph = json.load(f)

    # Recompute the expected output
    expected_strings = []
    for node, data in graph.items():
        val = data.get("val", "")
        reversed_val = val[::-1]
        expected_strings.append(reversed_val)

    expected_strings.sort()
    expected_output = "\n".join(expected_strings) + "\n"

    with open(output_path, "r") as f:
        actual_output = f.read()

    assert actual_output.strip() == expected_output.strip(), \
        f"Output in {output_path} does not match the expected sorted reversed strings."