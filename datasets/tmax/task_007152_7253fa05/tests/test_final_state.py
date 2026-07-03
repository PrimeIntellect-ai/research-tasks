# test_final_state.py

import os
import subprocess
import pytest

def test_fuzzer_script_exists():
    fuzzer_path = "/home/user/log_tool/fuzzer.py"
    assert os.path.isfile(fuzzer_path), f"Fuzzer script not found at {fuzzer_path}"

    # Basic check to ensure it is a python file
    with open(fuzzer_path, "r") as f:
        content = f.read()
    assert "import" in content or "print" in content or "subprocess" in content, "Fuzzer script does not look like valid Python code"

def test_makefile_fixed():
    makefile_path = "/home/user/log_tool/Makefile"
    assert os.path.isfile(makefile_path), f"Makefile not found at {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-lm" in content, "Makefile does not link the math library (-lm). The build will fail."

def test_c_code_fixed():
    c_file_path = "/home/user/log_tool/log_processor.c"
    assert os.path.isfile(c_file_path), f"C source file not found at {c_file_path}"

    with open(c_file_path, "r") as f:
        content = f.read()

    # Check that integer division is removed or fixed
    assert "5 / 9" not in content, "The integer division bug (5 / 9) is still present in log_processor.c"

    # Check that the memory corruption bug is addressed
    assert "(unsigned int*)&out_buffer[i]" not in content, "The memory corruption bug in sscanf is still present in log_processor.c"

def test_executable_compiles_and_runs():
    cwd = "/home/user/log_tool"

    # Run make to ensure it builds successfully
    make_result = subprocess.run(["make"], cwd=cwd, capture_output=True, text=True)
    assert make_result.returncode == 0, f"make failed:\n{make_result.stderr}"

    exe_path = os.path.join(cwd, "log_processor")
    assert os.path.isfile(exe_path), "log_processor executable was not built"

    # Run the executable with raw_logs.txt
    raw_logs_path = os.path.join(cwd, "raw_logs.txt")
    with open(raw_logs_path, "r") as f:
        raw_logs_data = f.read()

    run_result = subprocess.run([exe_path], input=raw_logs_data, capture_output=True, text=True)
    assert run_result.returncode == 0, f"log_processor crashed or failed:\n{run_result.stderr}"

    # Check output
    expected_output = "N: 10, Adj: 5.00\nN: 20, Adj: 20.00\nN: 5, Adj: 1.25\n"
    assert run_result.stdout == expected_output, f"log_processor produced incorrect output:\n{run_result.stdout}"

def test_fixed_metrics_file():
    metrics_path = "/home/user/log_tool/fixed_metrics.txt"
    assert os.path.isfile(metrics_path), f"Output file not found at {metrics_path}"

    with open(metrics_path, "r") as f:
        content = f.read()

    expected_output = "N: 10, Adj: 5.00\nN: 20, Adj: 20.00\nN: 5, Adj: 1.25\n"
    assert content.strip() == expected_output.strip(), f"The contents of {metrics_path} do not match the expected output."