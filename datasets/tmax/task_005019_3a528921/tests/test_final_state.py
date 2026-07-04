# test_final_state.py

import os
import subprocess
import pytest

def test_source_file_exists():
    assert os.path.isfile('/home/user/analyze_graph.c'), "Source file /home/user/analyze_graph.c does not exist."

def test_compilation():
    # Compile the code to ensure we are testing the latest version
    result = subprocess.run(
        ['gcc', '/home/user/analyze_graph.c', '-o', '/home/user/analyze'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Compilation failed:\n{result.stderr}"
    assert os.path.isfile('/home/user/analyze'), "Executable /home/user/analyze was not created."

def test_analyze_output_1():
    # Test case from the prompt: min_year=2018, page_size=3, page_number=2
    result = subprocess.run(
        ['/home/user/analyze', '2018', '3', '2'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Execution failed:\n{result.stderr}"

    expected_output = "p4,1\np7,1\np6,0"
    actual_output = result.stdout.strip()
    assert actual_output == expected_output, f"Expected output:\n{expected_output}\n\nGot:\n{actual_output}"

def test_analyze_output_2():
    # Test case: min_year=2019, page_size=2, page_number=1
    # Valid nodes: p3, p4, p5, p7
    # Valid edges: p7->p4, p7->p5, p4->p5, p3->p5
    # In-degrees: p5: 3, p4: 1, p3: 0, p7: 0
    # Sorted: p5,3 | p4,1 | p3,0 | p7,0
    # Page 1, size 2 -> p5,3 | p4,1
    result = subprocess.run(
        ['/home/user/analyze', '2019', '2', '1'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Execution failed:\n{result.stderr}"

    expected_output = "p5,3\np4,1"
    actual_output = result.stdout.strip()
    assert actual_output == expected_output, f"Expected output:\n{expected_output}\n\nGot:\n{actual_output}"

def test_analyze_output_3():
    # Test case: min_year=2022, page_size=5, page_number=1
    # Valid nodes: p7
    # Valid edges: none
    # In-degrees: p7: 0
    # Sorted: p7,0
    # Page 1, size 5 -> p7,0
    result = subprocess.run(
        ['/home/user/analyze', '2022', '5', '1'],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"Execution failed:\n{result.stderr}"

    expected_output = "p7,0"
    actual_output = result.stdout.strip()
    assert actual_output == expected_output, f"Expected output:\n{expected_output}\n\nGot:\n{actual_output}"