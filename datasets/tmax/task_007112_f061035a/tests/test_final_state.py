# test_final_state.py
import os
import subprocess

def test_solution_file_content():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"{solution_path} does not exist. Did you save your answer?"

    with open(solution_path, "r") as f:
        content = f.read().strip()

    assert content == "20937", f"Expected solution to be '20937', but found '{content}'"

def test_cpp_code_fixed():
    cpp_path = "/home/user/telemetry/telemetry_processor.cpp"
    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."

    with open(cpp_path, "r") as f:
        code = f.read()

    expected_error_msg = "Buffer overflow during varint decoding"
    assert expected_error_msg in code, (
        f"The C++ code does not contain the exact expected exception message: '{expected_error_msg}'"
    )

def test_binary_compiled_and_runs():
    binary_path = "/home/user/telemetry/telemetry_processor"
    data_path = "/home/user/telemetry/data.bin"

    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} does not exist. Did you run 'make'?"
    assert os.access(binary_path, os.X_OK), f"{binary_path} is not executable."
    assert os.path.isfile(data_path), f"{data_path} does not exist. Did you run generate_traffic.py?"

    # Run the binary and check its output
    result = subprocess.run([binary_path, data_path], capture_output=True, text=True)

    # The process should catch the exception and exit gracefully (return code 0)
    assert result.returncode == 0, f"telemetry_processor crashed or exited with an error. Return code: {result.returncode}"

    output = result.stdout + result.stderr
    assert "Buffer overflow during varint decoding" in output, (
        "Output did not contain the expected error message from the caught exception."
    )
    assert "20937" in output, "Output did not contain the expected Total Sum (20937)."