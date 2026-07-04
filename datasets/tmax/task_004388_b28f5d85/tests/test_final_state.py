# test_final_state.py

import os
import time
import subprocess
import pytest

def test_artifact_scanner_correctness_and_speedup():
    ref_script = "/home/user/reference_scanner.py"
    cpp_binary = "/home/user/artifact_scanner"
    output_csv = "/home/user/scan_results.csv"

    # Ensure the compiled C++ scanner exists and is executable
    assert os.path.isfile(cpp_binary), f"Compiled executable not found at {cpp_binary}"
    assert os.access(cpp_binary, os.X_OK), f"File is not executable: {cpp_binary}"

    # Clean up any existing output CSV
    if os.path.exists(output_csv):
        os.remove(output_csv)

    # 1. Run and time the reference Python scanner
    start_time_ref = time.time()
    try:
        subprocess.run(["python3", ref_script], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Reference scanner failed to run: {e.stderr}")
    ref_time = time.time() - start_time_ref

    assert os.path.isfile(output_csv), f"Reference scanner did not produce {output_csv}"

    # Read the reference results
    with open(output_csv, 'r', encoding='utf-8') as f:
        ref_results = [line.strip() for line in f if line.strip()]

    # Clean up CSV for the C++ run
    os.remove(output_csv)

    # 2. Run and time the optimized C++ scanner
    start_time_cpp = time.time()
    try:
        subprocess.run([cpp_binary], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"C++ scanner failed to run: {e.stderr}")
    cpp_time = time.time() - start_time_cpp

    assert os.path.isfile(output_csv), f"C++ scanner did not produce {output_csv}"

    # Read the C++ results
    with open(output_csv, 'r', encoding='utf-8') as f:
        cpp_results = [line.strip() for line in f if line.strip()]

    # 3. Verify correctness
    # The C++ scanner might process files in a different order due to multithreading,
    # so we compare the sets of lines.
    assert len(ref_results) == 10000, f"Expected 10,000 lines from reference, got {len(ref_results)}"
    assert len(cpp_results) == 10000, f"Expected 10,000 lines from C++ scanner, got {len(cpp_results)}"

    ref_set = set(ref_results)
    cpp_set = set(cpp_results)

    missing_in_cpp = ref_set - cpp_set
    extra_in_cpp = cpp_set - ref_set

    if missing_in_cpp or extra_in_cpp:
        error_msg = "C++ scanner output does not match reference output.\n"
        if missing_in_cpp:
            error_msg += f"Missing entries (sample): {list(missing_in_cpp)[:5]}\n"
        if extra_in_cpp:
            error_msg += f"Extra/incorrect entries (sample): {list(extra_in_cpp)[:5]}\n"
        pytest.fail(error_msg)

    # 4. Verify performance metric (speedup >= 3.0)
    speedup = ref_time / cpp_time
    assert speedup >= 3.0, (
        f"Performance threshold not met! "
        f"Reference time: {ref_time:.3f}s, C++ time: {cpp_time:.3f}s. "
        f"Speedup: {speedup:.2f}x (Required: >= 3.0x)"
    )