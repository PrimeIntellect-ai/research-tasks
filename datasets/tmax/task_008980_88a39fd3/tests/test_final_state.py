# test_final_state.py

import os
import subprocess
import pytest

BASE_DIR = "/home/user/data_migration"

def test_cmake_and_build():
    cmake_file = os.path.join(BASE_DIR, "c_src", "CMakeLists.txt")
    assert os.path.isfile(cmake_file), f"Missing file: {cmake_file}"

    with open(cmake_file, "r") as f:
        content = f.read()
        assert "target_link_libraries" in content and not content.startswith("# target_link_libraries"), "CMakeLists.txt does not link libraries properly."

    calc_node_exec = os.path.join(BASE_DIR, "c_src", "build", "calc_node")
    assert os.path.isfile(calc_node_exec), f"Missing executable: {calc_node_exec}. Did you build the project?"

    # Run the executable to ensure it works and libraries are linked
    try:
        result = subprocess.run(
            [calc_node_exec, "10"],
            capture_output=True,
            text=True,
            check=True
        )
        # transform(10) = (10 ^ 0x5A) + 12 = (10 ^ 90) + 12 = 80 + 12 = 92
        assert result.stdout.strip() == "92", f"calc_node produced incorrect output: {result.stdout.strip()}"
    except subprocess.CalledProcessError as e:
        pytest.fail(f"calc_node execution failed: {e.stderr}")

def test_python_parser_migrated():
    parser_file = os.path.join(BASE_DIR, "dag_parser.py")
    assert os.path.isfile(parser_file), f"Missing file: {parser_file}"

    with open(parser_file, "r") as f:
        content = f.read()
        assert "print(" in content or "print (" in content, "dag_parser.py still contains Python 2 print statements."
        assert "xrange" not in content, "dag_parser.py still contains Python 2 xrange."

    # Run the parser with Python 3
    test_node = os.path.join(BASE_DIR, "nodes", "leaf1.node")
    try:
        result = subprocess.run(
            ["python3", parser_file, test_node],
            capture_output=True,
            text=True,
            check=True
        )
        assert "VALUE: 10" in result.stdout, "dag_parser.py did not output the correct VALUE."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"dag_parser.py failed to run under Python 3: {e.stderr}")

def test_process_graph_script():
    script_file = os.path.join(BASE_DIR, "process_graph.sh")
    assert os.path.isfile(script_file), f"Missing file: {script_file}"
    assert os.access(script_file, os.X_OK), f"{script_file} is not executable."

def test_result_output():
    result_file = os.path.join(BASE_DIR, "result.txt")
    assert os.path.isfile(result_file), f"Missing result file: {result_file}. Did you run the script?"

    with open(result_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "Processed: leaf1",
        "Processed: child1",
        "Processed: leaf2",
        "Processed: child2",
        "Processed: root",
        "Final Accumulator: 11555"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in result.txt, found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch. Expected '{expected}', got '{actual}'."