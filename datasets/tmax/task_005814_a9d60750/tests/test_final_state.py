# test_final_state.py

import os
import subprocess

def test_shared_libraries_exist():
    math_so = "/home/user/project/build/libmath_ops.so"
    rust_so = "/home/user/project/build/librust_compute.so"

    assert os.path.isfile(math_so), f"Missing shared library: {math_so}"
    assert os.path.isfile(rust_so), f"Missing shared library: {rust_so}"

def test_exit42_executable():
    exe_path = "/home/user/project/build/exit42"
    assert os.path.isfile(exe_path), f"Missing executable: {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File is not executable: {exe_path}"

    # Run the executable and check the exit code
    result = subprocess.run([exe_path], capture_output=True)
    assert result.returncode == 42, f"Expected exit code 42, got {result.returncode}"

def test_results_sorted():
    results_path = "/home/user/project/output/results_sorted.txt"
    assert os.path.isfile(results_path), f"Missing results file: {results_path}"

    with open(results_path, "r") as f:
        content = f.read().strip()

    expected = "TestA: 6\nTestB: 10\nTestC: 60"
    assert content == expected, f"Output mismatch in {results_path}.\nExpected:\n{expected}\nGot:\n{content}"

def test_rust_compiles():
    rust_file = "/home/user/project/src/lib.rs"
    assert os.path.isfile(rust_file), f"Missing Rust source file: {rust_file}"

    # Run rustc to check if it compiles (borrow checker passes)
    # Using --emit=metadata checks syntax and types without attempting to link the C library
    result = subprocess.run(
        ["rustc", "--crate-type", "lib", "--emit=metadata", rust_file, "-o", "/tmp/lib_test.rmeta"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Rust compilation failed (borrow checker error still present?):\n{result.stderr}"

def test_build_and_run_script_exists():
    script_path = "/home/user/project/build_and_run.sh"
    assert os.path.isfile(script_path), f"Missing orchestration script: {script_path}"