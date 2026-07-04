# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_libmetrics_so_exists():
    """Ensure the compiled dynamic library exists."""
    assert os.path.isfile("/home/user/libmetrics.so"), "/home/user/libmetrics.so does not exist. Did you compile the Rust code to a dynamic library?"

def test_bench_run_exists():
    """Ensure the compiled C executable exists."""
    assert os.path.isfile("/home/user/bench_run"), "/home/user/bench_run does not exist. Did you compile bench.c?"
    assert os.access("/home/user/bench_run", os.X_OK), "/home/user/bench_run is not executable."

def test_bench_output_correct():
    """Ensure the benchmark output matches the expected moving average calculations."""
    output_path = "/home/user/bench_output.txt"
    assert os.path.isfile(output_path), f"{output_path} does not exist. Did you run bench_run and redirect its output?"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Avg after 10.0: 10.0",
        "Avg after 20.0: 15.0",
        "Avg after 30.0: 20.0",
        "Avg after 40.0: 30.0",
        "Avg after 50.0: 40.0",
        "Execution completed."
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"Output in {output_path} does not match expected moving averages."

def test_ffi_correctness_with_custom_c_program():
    """Compile a new C program against libmetrics.so to verify FFI correctness independently."""
    c_code = """
#include <stdio.h>
#include <stddef.h>

extern void init_metrics(size_t capacity);
extern double record_and_average(double latency);

int main() {
    init_metrics(2);
    printf("%.1f\\n", record_and_average(100.0));
    printf("%.1f\\n", record_and_average(200.0));
    printf("%.1f\\n", record_and_average(300.0));
    return 0;
}
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        c_file = os.path.join(tmpdir, "test_ffi.c")
        exe_file = os.path.join(tmpdir, "test_ffi_run")

        with open(c_file, "w") as f:
            f.write(c_code)

        # Compile
        compile_cmd = [
            "gcc", c_file, "-o", exe_file, 
            "-L/home/user", "-lmetrics",
            "-Wl,-rpath=/home/user"
        ]

        try:
            subprocess.run(compile_cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to compile test C program against libmetrics.so. Error: {e.stderr}")

        # Run
        env = os.environ.copy()
        env["LD_LIBRARY_PATH"] = "/home/user" + (":" + env["LD_LIBRARY_PATH"] if "LD_LIBRARY_PATH" in env else "")

        try:
            result = subprocess.run([exe_file], check=True, capture_output=True, text=True, env=env)
            output = result.stdout.strip().splitlines()

            assert len(output) == 3, "Expected 3 lines of output from test FFI program."
            assert output[0] == "100.0", f"Expected 100.0, got {output[0]}"
            assert output[1] == "150.0", f"Expected 150.0, got {output[1]}"
            assert output[2] == "250.0", f"Expected 250.0, got {output[2]}"

        except subprocess.CalledProcessError as e:
            pytest.fail(f"Failed to run test C program against libmetrics.so. Error: {e.stderr}")