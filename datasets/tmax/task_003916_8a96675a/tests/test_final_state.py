# test_final_state.py

import os
import subprocess
import pytest

def test_import_succeeds():
    """Verify that importing graph_wrapper succeeds after fixing the RPATH."""
    res = subprocess.run(
        ["python3", "-c", "import graph_wrapper"],
        cwd="/home/user/mathlib",
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, f"Importing graph_wrapper still fails. Error:\n{res.stderr}"

def test_rpath_configured():
    """Verify that libgraph.so has the correct RPATH set."""
    lib_path = "/home/user/mathlib/lib/libgraph.so"
    assert os.path.exists(lib_path), f"Library {lib_path} does not exist. Did you run build.sh?"

    res = subprocess.run(["readelf", "-d", lib_path], capture_output=True, text=True)
    assert res.returncode == 0, "Failed to run readelf on libgraph.so"

    stdout_lower = res.stdout.lower()
    assert "rpath" in stdout_lower or "runpath" in stdout_lower, "RPATH/RUNPATH is not set in libgraph.so"
    assert "/home/user/mathlib/lib" in res.stdout, "RPATH does not point to the absolute path /home/user/mathlib/lib"

def test_dependencies_installed():
    """Verify that pytest and hypothesis are installed."""
    res = subprocess.run(
        ["python3", "-c", "import pytest; import hypothesis"],
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, "pytest and/or hypothesis are not installed in the Python environment"

def test_test_graph_file_and_content():
    """Verify that test_graph.py exists and contains the required test functions."""
    test_file = "/home/user/mathlib/test_graph.py"
    assert os.path.exists(test_file), f"Test file {test_file} is missing"

    with open(test_file, "r") as f:
        content = f.read()

    assert "test_zero_matrix_paths" in content, "Function 'test_zero_matrix_paths' not found in test_graph.py"
    assert "test_zero_steps" in content, "Function 'test_zero_steps' not found in test_graph.py"
    assert "hypothesis" in content, "hypothesis does not appear to be used in test_graph.py"

def test_pytest_passes():
    """Verify that running pytest on test_graph.py succeeds."""
    res = subprocess.run(
        ["python3", "-m", "pytest", "/home/user/mathlib/test_graph.py"],
        capture_output=True,
        text=True
    )
    assert res.returncode == 0, f"pytest failed on test_graph.py. Output:\n{res.stdout}\n{res.stderr}"