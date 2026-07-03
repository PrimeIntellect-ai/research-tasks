# test_final_state.py

import os
import re

def test_cargo_toml_cdylib():
    path = "/home/user/rust_ffi_project/sorter/Cargo.toml"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    # Looking for crate-type = ["cdylib"]
    assert "cdylib" in content, "Cargo.toml is missing 'cdylib' crate-type configuration."

def test_lib_rs_fixes():
    path = "/home/user/rust_ffi_project/sorter/src/lib.rs"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "#[no_mangle]" in content, "lib.rs is missing #[no_mangle] directive for the FFI functions."
    assert "extern \"C\"" in content, "lib.rs is missing extern \"C\" directive for the FFI functions."

def test_shared_library_exists():
    path = "/home/user/rust_ffi_project/sorter/target/release/libsorter.so"
    assert os.path.isfile(path), f"Compiled shared library not found at {path}. Make sure you built it with --release."

def test_benchmark_script_exists():
    path = "/home/user/rust_ffi_project/benchmark.py"
    assert os.path.isfile(path), f"Python script not found at {path}."

def test_verification_txt():
    path = "/home/user/rust_ffi_project/verification.txt"
    assert os.path.isfile(path), f"Verification file not found at {path}. Did the benchmark script run successfully?"
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "MATCH", f"Expected 'MATCH' in verification.txt, but got '{content}'."

def test_report_txt():
    path = "/home/user/rust_ffi_project/report.txt"
    assert os.path.isfile(path), f"Report file not found at {path}. Did the benchmark script run successfully?"
    with open(path, "r") as f:
        content = f.read().strip()

    # Check if the output matches the required format exactly
    pattern = r"^Algorithm: Merge Sort, Avg Time: \d+\.\d{4} seconds\nAlgorithm: Quick Sort, Avg Time: \d+\.\d{4} seconds$"
    assert re.match(pattern, content), "report.txt does not match the expected format with 4 decimal places."