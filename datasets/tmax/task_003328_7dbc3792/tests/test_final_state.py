# test_final_state.py

import os
import ast

def test_process_py_syntax():
    script_path = "/home/user/migration/process.py"
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "print " not in content, "process.py still contains Python 2 print statements."
    assert "xrange" not in content, "process.py still contains Python 2 xrange."

    try:
        ast.parse(content)
    except SyntaxError as e:
        pytest.fail(f"process.py contains a Python 3 syntax error: {e}")

def test_libprocessor_so_exists():
    # The user might build it in /home/user/migration/src or /home/user/migration/src/build
    # Let's search for it in /home/user/migration
    base_dir = "/home/user/migration"
    found = False
    for root, dirs, files in os.walk(base_dir):
        if "libprocessor.so" in files:
            found = True
            break
    assert found, "libprocessor.so was not found. The CMake project was not compiled correctly."

def test_diff_result_empty():
    diff_path = "/home/user/migration/diff_result.txt"
    assert os.path.isfile(diff_path), f"{diff_path} is missing."

    with open(diff_path, 'r') as f:
        content = f.read().strip()

    assert content == "", f"diff_result.txt is not empty. Differences found:\n{content}"

def test_execution_order_valid():
    order_path = "/home/user/migration/execution_order.txt"
    assert os.path.isfile(order_path), f"{order_path} is missing."

    with open(order_path, 'r') as f:
        content = f.read().strip()

    order = [x.strip() for x in content.split(',') if x.strip()]

    expected_files = {
        "data_A.txt", "data_B.txt", "data_C.txt", 
        "data_D.txt", "data_E.txt", "data_F.txt"
    }

    assert set(order) == expected_files, f"execution_order.txt does not contain exactly the required files. Found: {order}"

    # Check topological constraints
    # A -> B -> C -> F
    # A -> D -> E -> F
    def assert_before(dep, target):
        assert order.index(dep) < order.index(target), f"Topological sort failed: {dep} must be executed before {target}"

    assert_before("data_A.txt", "data_B.txt")
    assert_before("data_A.txt", "data_D.txt")
    assert_before("data_B.txt", "data_C.txt")
    assert_before("data_D.txt", "data_E.txt")
    assert_before("data_C.txt", "data_F.txt")
    assert_before("data_E.txt", "data_F.txt")

def test_final_output_exists():
    output_path = "/home/user/migration/final_output.txt"
    assert os.path.isfile(output_path), f"{output_path} is missing."

    with open(output_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) == 6, f"final_output.txt should contain 6 lines, but found {len(lines)}."