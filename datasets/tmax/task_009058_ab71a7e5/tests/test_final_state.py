# test_final_state.py
import os
import subprocess
import pytest

def test_fuzz_sh_exists_and_executable():
    fuzz_path = "/home/user/fuzz.sh"
    assert os.path.isfile(fuzz_path), f"File {fuzz_path} does not exist."
    assert os.access(fuzz_path, os.X_OK), f"File {fuzz_path} is not executable."

    with open(fuzz_path, 'r') as f:
        content = f.read()

    assert "processor" in content, f"{fuzz_path} does not appear to run the processor executable."
    assert "for" in content or "while" in content, f"{fuzz_path} does not appear to contain a loop."

def test_concurrent_processor_fixed():
    cpp_path = "/home/user/concurrent_processor.cpp"
    assert os.path.isfile(cpp_path), f"File {cpp_path} does not exist."

    with open(cpp_path, 'r') as f:
        content = f.read()

    has_atomic = "std::atomic" in content
    has_mutex = "std::mutex" in content or "pthread_mutex" in content

    assert has_atomic or has_mutex, f"{cpp_path} does not seem to use std::atomic or a mutex to fix the race condition."

def test_final_result_txt():
    result_path = "/home/user/final_result.txt"
    assert os.path.isfile(result_path), f"File {result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content == "500000", f"{result_path} contains '{content}', expected '500000'."

def test_processor_fixed_executable():
    exe_path = "/home/user/processor_fixed"
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    # Run multiple times to ensure no race condition remains
    for _ in range(20):
        result = subprocess.run([exe_path, "1000000"], capture_output=True, text=True)
        assert result.returncode == 0, f"Execution of {exe_path} failed."
        output = result.stdout.strip()
        assert output == "1000000", f"Expected output 1000000, but got {output}. Race condition might still exist."