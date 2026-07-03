# test_final_state.py

import os
import subprocess
import pytest

def test_make_all_succeeds():
    """Verify that the Makefile has been fixed and builds successfully."""
    work_dir = "/home/user/url_router"

    # Run make clean
    subprocess.run(["make", "clean"], cwd=work_dir, capture_output=True)

    # Run make all
    result = subprocess.run(["make", "all"], cwd=work_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"make all failed. stderr:\n{result.stderr}\nstdout:\n{result.stdout}"

    # Check if executables exist
    assert os.path.isfile(os.path.join(work_dir, "router_app")), "router_app executable was not built"
    assert os.path.isfile(os.path.join(work_dir, "router_test")), "router_test executable was not built"

def test_router_bug_fixed():
    """Verify that the out-of-bounds bug in router.cpp is fixed."""
    test_code = """
#include "/home/user/url_router/router.h"
#include <iostream>
#include <cassert>

int main() {
    try {
        RouteResult r1 = Router::parse("/api?key=");
        if (r1.params["key"] != "") return 1;

        RouteResult r2 = Router::parse("/api?key");
        if (r2.params["key"] != "") return 2;

        RouteResult r3 = Router::parse("/api?key=&other=1");
        if (r3.params["key"] != "") return 3;
        if (r3.params["other"] != "1") return 4;
    } catch (...) {
        return 5;
    }
    return 0;
}
"""
    test_file = "/tmp/verify_bug.cpp"
    out_file = "/tmp/verify_bug"

    with open(test_file, "w") as f:
        f.write(test_code)

    # Compile the test with the user's router.cpp
    compile_cmd = ["g++", "-std=c++17", test_file, "/home/user/url_router/router.cpp", "-o", out_file]
    comp_res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert comp_res.returncode == 0, f"Failed to compile test against router.cpp:\n{comp_res.stderr}"

    # Run the test
    run_res = subprocess.run([out_file], capture_output=True, text=True)
    assert run_res.returncode == 0, f"Bug in router.cpp is not fixed. Test returned code {run_res.returncode}"

def test_benchmark_functionality():
    """Verify that running './router_app bench' writes the elapsed time to benchmark.log."""
    work_dir = "/home/user/url_router"
    log_file = "/home/user/benchmark.log"

    # Ensure a clean state
    if os.path.exists(log_file):
        os.remove(log_file)

    app_path = os.path.join(work_dir, "router_app")
    assert os.path.isfile(app_path), "router_app must be built before testing benchmark"

    # Run the benchmark
    result = subprocess.run([app_path, "bench"], cwd=work_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"router_app bench failed. stderr:\n{result.stderr}"

    # Check log file
    assert os.path.isfile(log_file), f"Benchmark log file {log_file} was not created"

    with open(log_file, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
        assert val >= 0, "Benchmark duration should be a non-negative number"
    except ValueError:
        pytest.fail(f"Log file {log_file} does not contain a valid numeric value. Found: '{content}'")