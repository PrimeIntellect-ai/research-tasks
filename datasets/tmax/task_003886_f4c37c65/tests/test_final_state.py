# test_final_state.py
import os
import subprocess

def test_files_exist():
    expected_files = [
        "/home/user/query_processor.cpp",
        "/home/user/query_processor",
        "/home/user/crashing_input.txt",
        "/home/user/regression_test.sh",
        "/home/user/diagnostics.log"
    ]
    for path in expected_files:
        assert os.path.isfile(path), f"File {path} is missing."

def test_query_processor_fixed_behavior():
    # Compile the source code to ensure it's valid
    compile_cmd = ["g++", "-O2", "-std=c++17", "/home/user/query_processor.cpp", "-o", "/tmp/test_query_processor"]
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Compilation failed: {res.stderr}"

    # Run with test input
    run_cmd = ["/tmp/test_query_processor", "a&b=c"]
    res = subprocess.run(run_cmd, capture_output=True, text=True)
    assert res.returncode == 0, "Program crashed on valid input 'a&b=c'."

    output = res.stdout.strip().split("\n")
    assert len(output) >= 2, "Output does not contain enough lines."
    assert output[0].strip() == "K:a V:", f"Expected 'K:a V:', got '{output[0]}'"
    assert output[1].strip() == "K:b V:c", f"Expected 'K:b V:c', got '{output[1]}'"

def test_crashing_input_content():
    with open("/home/user/crashing_input.txt", "r") as f:
        content = f.read().strip()

    assert content, "crashing_input.txt is empty."

    tokens = content.split("&")
    has_missing_eq = any("=" not in token for token in tokens)
    assert has_missing_eq, "crashing_input.txt does not contain a token without an '=' sign."

def test_regression_test_script():
    script_path = "/home/user/regression_test.sh"
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    res = subprocess.run([script_path], capture_output=True, text=True)
    assert res.returncode == 0, f"{script_path} did not exit with code 0."

def test_diagnostics_log():
    with open("/home/user/crashing_input.txt", "r") as f:
        input_str = f.read().strip()

    # Run the compiled binary to get expected output
    res = subprocess.run(["/home/user/query_processor", input_str], capture_output=True, text=True)
    assert res.returncode == 0, "query_processor crashed on crashing_input.txt."
    expected_output = res.stdout.strip()

    with open("/home/user/diagnostics.log", "r") as f:
        actual_output = f.read().strip()

    assert actual_output == expected_output, f"diagnostics.log content does not match expected output.\nExpected:\n{expected_output}\nActual:\n{actual_output}"