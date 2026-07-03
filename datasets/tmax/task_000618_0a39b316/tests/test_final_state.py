# test_final_state.py
import os
import re
import sys
import subprocess

def test_extracted_payloads():
    path = "/home/user/api_scanner/extracted_payloads.txt"
    assert os.path.exists(path), f"File {path} does not exist. Did you extract the payloads from the video?"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["1a2b3c", "4d5e6f", "7g8h9i", "0j1k2l", "3m4n5o"]
    assert lines == expected, f"Extracted payloads do not match the expected values from the video.\nExpected: {expected}\nGot: {lines}"

def test_scanner_import_order():
    path = "/home/user/api_scanner/scanner.py"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    fast_fuzzer_idx = content.find("import fast_fuzzer")
    requests_idx = content.find("import requests")
    ssl_idx = content.find("import ssl")

    assert fast_fuzzer_idx != -1, "import fast_fuzzer not found in scanner.py"
    assert requests_idx != -1, "import requests not found in scanner.py"
    assert ssl_idx != -1, "import ssl not found in scanner.py"

    assert fast_fuzzer_idx > requests_idx, "fast_fuzzer must be imported AFTER requests to fix the CI monkey-patching bug."
    assert fast_fuzzer_idx > ssl_idx, "fast_fuzzer must be imported AFTER ssl to fix the CI monkey-patching bug."

def test_benchmark_performance():
    path = "/home/user/api_scanner/benchmark.py"
    assert os.path.exists(path), f"Benchmark script {path} does not exist."

    env = os.environ.copy()
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"/home/user/api_scanner:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = "/home/user/api_scanner"

    # Run the benchmark script
    result = subprocess.run([sys.executable, path], capture_output=True, text=True, env=env)
    assert result.returncode == 0, f"benchmark.py failed with error:\n{result.stderr}"

    output = result.stdout
    match = re.search(r"Throughput:\s*([0-9]*\.?[0-9]+)\s*seconds", output)
    assert match is not None, f"Could not find 'Throughput: <float> seconds' in benchmark stdout.\nOutput was:\n{output}"

    execution_time = float(match.group(1))
    threshold = 0.25
    assert execution_time <= threshold, f"Benchmark execution time {execution_time} exceeds threshold of {threshold} seconds. The Rust extension might not be fully optimized or built in release mode."

def test_rust_extension_directly():
    env = os.environ.copy()
    if "PYTHONPATH" in env:
        env["PYTHONPATH"] = f"/home/user/api_scanner:{env['PYTHONPATH']}"
    else:
        env["PYTHONPATH"] = "/home/user/api_scanner"

    code = """
import time
import fast_fuzzer

payloads = ["1a2b3c", "4d5e6f", "7g8h9i", "0j1k2l", "3m4n5o"]
start = time.time()
for _ in range(10000):
    for p in payloads:
        fast_fuzzer.process_payload(p)
end = time.time()
print(end - start)
"""
    result = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env)
    assert result.returncode == 0, f"Failed to import and run fast_fuzzer directly. Is the .so file built and in /home/user/api_scanner?\nError:\n{result.stderr}"

    execution_time = float(result.stdout.strip())
    threshold = 0.25
    assert execution_time <= threshold, f"Direct execution time {execution_time} exceeds threshold of {threshold} seconds. Ensure lib.rs borrows &str and is built in release mode."

def test_lib_rs_optimized():
    path = "/home/user/api_scanner/src/lib.rs"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "&str" in content, "lib.rs does not seem to use &str for string borrowing. You should borrow the string slice from Python instead of taking ownership."