# test_final_state.py

import os
import pytest

def test_execution_order_output():
    output_path = "/home/user/execution_order.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did you run the pipeline and redirect the output?"

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    valid_sort_1 = ['A', 'B', 'C', 'D', 'E']
    valid_sort_2 = ['A', 'C', 'B', 'D', 'E']

    assert lines == valid_sort_1 or lines == valid_sort_2, (
        f"The execution order in {output_path} is incorrect. "
        f"Expected {valid_sort_1} or {valid_sort_2}, but got {lines}."
    )

def test_pipeline_py_is_valid_python3():
    pipeline_path = "/home/user/pipeline.py"
    assert os.path.isfile(pipeline_path), f"File {pipeline_path} is missing."

    with open(pipeline_path, 'r') as f:
        code = f.read()

    try:
        compile(code, pipeline_path, 'exec')
    except SyntaxError as e:
        pytest.fail(f"{pipeline_path} contains a Python 3 SyntaxError: {e}. Ensure all Python 2 syntax (like print statements) is fixed.")

def test_graph_solver_c_fixed():
    c_path = "/home/user/graph_solver.c"
    assert os.path.isfile(c_path), f"File {c_path} is missing."

    with open(c_path, 'r') as f:
        code = f.read()

    # The original buggy code had exactly this line inside solve_graph()
    buggy_line = "int sorted_nodes[26];"
    assert buggy_line not in code, (
        f"{c_path} still contains the buggy local array allocation: '{buggy_line}'. "
        "You must allocate this array dynamically (e.g., malloc) or make it static."
    )

def test_graph_solver_compiled():
    exe_path = "/home/user/graph_solver"
    assert os.path.isfile(exe_path), f"Compiled executable {exe_path} does not exist. Did you run build.sh?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."