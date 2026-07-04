# test_final_state.py
import os
import subprocess

def test_router_compiled():
    router_path = "/home/user/router/router"
    assert os.path.isfile(router_path), f"{router_path} does not exist. Did you run make?"
    assert os.access(router_path, os.X_OK), f"{router_path} is not executable."

def test_router_test_output():
    router_path = "/home/user/router/router"
    # Ensure the binary exists before trying to run it
    assert os.path.isfile(router_path), f"{router_path} does not exist."

    try:
        result = subprocess.run([router_path, "test"], capture_output=True, text=True, timeout=5)
    except Exception as e:
        assert False, f"Failed to execute {router_path} test: {e}"

    assert result.returncode == 0, f"Expected exit code 0, got {result.returncode}. Output: {result.stdout}"
    assert result.stdout.strip() == "ALL TESTS PASSED", f"Expected 'ALL TESTS PASSED', got '{result.stdout.strip()}'"

def test_benchmark_result():
    result_path = "/home/user/benchmark_result.txt"
    assert os.path.isfile(result_path), f"Benchmark result file {result_path} does not exist."

    with open(result_path, "r") as f:
        content = f.read()

    assert content.strip() == "Parsed 100000 URLs", f"Expected 'Parsed 100000 URLs' in {result_path}, got '{content.strip()}'"