# test_final_state.py

import os
import subprocess
import pytest

TASK_DIR = "/home/user/abi_task"
SHIM_S = os.path.join(TASK_DIR, "shim.s")
SHIM_SO = os.path.join(TASK_DIR, "libshim.so")
FINAL_SYMBOLS = os.path.join(TASK_DIR, "final_symbols.txt")

EXPECTED_SYMBOLS = [
    "core_process",
    "legacy_hash_func",
    "matrix_transform_v1",
    "matrix_transform_v2",
    "optimize_path",
    "validate_state"
]

def test_shim_assembly_exists():
    assert os.path.isfile(SHIM_S), f"Assembly shim file not found at {SHIM_S}"

def test_shim_library_exists():
    assert os.path.isfile(SHIM_SO), f"Compiled shim library not found at {SHIM_SO}"

def test_shim_exports_missing_symbols():
    # Use nm to check exported dynamic symbols
    try:
        output = subprocess.check_output(['nm', '-D', SHIM_SO], stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to run nm on {SHIM_SO}: {e.output.decode('utf-8')}")
    except FileNotFoundError:
        pytest.fail("The 'nm' tool is not available.")

    # Parse exported symbols (typically marked 'T' or 'W' etc.)
    exported_symbols = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[1] in ('T', 'W'):
            exported_symbols.append(parts[2])

    assert 'legacy_hash_func' in exported_symbols, "libshim.so is missing the export for 'legacy_hash_func'"
    assert 'matrix_transform_v1' in exported_symbols, "libshim.so is missing the export for 'matrix_transform_v1'"

def test_final_symbols_file():
    assert os.path.isfile(FINAL_SYMBOLS), f"Final symbols file not found at {FINAL_SYMBOLS}"

    with open(FINAL_SYMBOLS, 'r') as f:
        actual_symbols = [line.strip() for line in f if line.strip()]

    assert actual_symbols == EXPECTED_SYMBOLS, (
        f"Contents of {FINAL_SYMBOLS} do not match the expected list.\n"
        f"Expected: {EXPECTED_SYMBOLS}\n"
        f"Actual: {actual_symbols}"
    )