# test_final_state.py
import os
import json
import subprocess

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.isfile(results_path), f"{results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{results_path} is not valid JSON."

    expected = {
        "105": True,
        "110": False,
        "135": True,
        "140": False,
        "210": True,
        "250": False
    }

    for k, v in expected.items():
        assert str(k) in data, f"Key '{k}' missing in results.json"
        assert data[str(k)] is v, f"Expected target '{k}' to be {v}, got {data[str(k)]}."

def test_libsolver_shared_object():
    so_path = "/home/user/solver/libsolver.so"
    assert os.path.isfile(so_path), f"{so_path} does not exist. The Makefile might not have compiled it."

    # Check if it's a shared object using the ELF header
    with open(so_path, "rb") as f:
        magic = f.read(4)
        assert magic == b"\x7fELF", f"{so_path} is not a valid ELF file."
        f.seek(16)
        e_type = int.from_bytes(f.read(2), byteorder="little")
        # e_type == 3 corresponds to ET_DYN (Shared object file)
        assert e_type == 3, f"{so_path} is not compiled as a shared object library. Ensure -shared and -fPIC were used."

def test_solve_api_exists_and_uses_ctypes():
    api_path = "/home/user/solve_api.py"
    assert os.path.isfile(api_path), f"{api_path} does not exist."

    with open(api_path, "r") as f:
        content = f.read()

    assert "ctypes" in content, f"{api_path} does not appear to use the 'ctypes' module."

def test_solver_c_fixed():
    c_path = "/home/user/solver/solver.c"
    assert os.path.isfile(c_path), f"{c_path} does not exist."

    with open(c_path, "r") as f:
        content = f.read()

    # The original buggy line that caused undefined behavior
    buggy_malloc = "malloc(target * sizeof(int))"
    assert buggy_malloc not in content, "solver.c still contains the memory safety bug (allocating exactly 'target' elements instead of 'target + 1')."