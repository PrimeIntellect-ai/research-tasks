# test_final_state.py

import os
import json
import subprocess
import pytest

def test_libmathops_exists():
    """Test that the shared library libmathops.so was created."""
    lib_path = "/home/user/math_port/libmathops.so"
    assert os.path.isfile(lib_path), f"Shared library {lib_path} is missing."

def test_math_router_exists_and_linked():
    """Test that math_router exists and is dynamically linked to libmathops.so."""
    router_path = "/home/user/math_port/math_router"
    assert os.path.isfile(router_path), f"Executable {router_path} is missing."

    # Check dynamic linkage
    ldd_out = subprocess.run(["ldd", router_path], capture_output=True, text=True)
    assert "libmathops.so" in ldd_out.stdout, "math_router is not dynamically linked against libmathops.so."

def test_container_out_json():
    """Test that the output JSON matches the expected sorted sequence."""
    out_path = "/home/user/container_out.json"
    assert os.path.isfile(out_path), f"Output file {out_path} is missing."

    with open(out_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{out_path} does not contain valid JSON.")

    expected = {"result": [4, 8, 15, 16, 23, 42]}
    assert data == expected, f"Content of {out_path} is incorrect. Expected {expected}, got {data}."

def test_valgrind_no_leaks():
    """Test that running the executable through Valgrind reports no leaks."""
    router_path = "/home/user/math_port/math_router"
    assert os.path.isfile(router_path), f"Executable {router_path} is missing."

    env = os.environ.copy()
    # Add the current directory to LD_LIBRARY_PATH so the shared library is found
    env["LD_LIBRARY_PATH"] = "/home/user/math_port:" + env.get("LD_LIBRARY_PATH", "")

    cmd = [
        "valgrind", 
        "--leak-check=full", 
        "--error-exitcode=1", 
        router_path, 
        "/math/merge?seq1=42,15,8&seq2=4,16,23"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert result.returncode == 0, f"Valgrind reported memory leaks or execution failed. stderr:\n{result.stderr}"

def test_api_diff():
    """Test that the API diff file exists and contains the correct unified diff output."""
    diff_path = "/home/user/api_diff.txt"
    assert os.path.isfile(diff_path), f"Diff file {diff_path} is missing."

    with open(diff_path, "r") as f:
        content = f.read()

    # A valid unified diff should have the removed legacy line and the added new line
    expected_removed = '-{"result": [1, 4, 8, 15, 16, 23, 42]}'
    expected_added = '+{"result": [4, 8, 15, 16, 23, 42]}'

    assert expected_removed in content, f"api_diff.txt is missing the expected removed line: {expected_removed}"
    assert expected_added in content, f"api_diff.txt is missing the expected added line: {expected_added}"