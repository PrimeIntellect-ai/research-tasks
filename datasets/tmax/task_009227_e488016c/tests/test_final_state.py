# test_final_state.py

import os
import subprocess

def test_c_source_exists():
    assert os.path.exists("/home/user/log_processor.c"), "The source file /home/user/log_processor.c is missing."

def test_executable_exists():
    assert os.path.exists("/home/user/log_processor"), "The executable /home/user/log_processor is missing."
    assert os.access("/home/user/log_processor", os.X_OK), "/home/user/log_processor is not executable."

def test_processed_log_content():
    expected_content = """99 10.0.0.1 PRE
100 10.0.0.1 START
100 10.0.0.2 START
101 10.0.0.1 ACTION
101 10.0.0.2 ACTION
102 10.0.0.1 ACTION
102 10.0.0.2 END
102 10.0.0.3 START
105 10.0.0.1 END
"""
    assert os.path.exists("/home/user/processed.log"), "/home/user/processed.log is missing."
    with open("/home/user/processed.log", "r") as f:
        content = f.read()
    assert content == expected_content, "Content of /home/user/processed.log does not match expected output for the provided logs."

def test_hidden_test_case():
    # Compile the code to ensure it's valid C
    compile_cmd = ["gcc", "-O3", "/home/user/log_processor.c", "-o", "/tmp/log_processor_test"]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Compilation failed:\n{result.stderr}"

    # Create hidden test files
    log1 = "/tmp/hidden_server1.log"
    log2 = "/tmp/hidden_server2.log"

    with open(log1, "w") as f:
        f.write("10 10.0.0.1 A\n20 10.0.0.1 B\n20 10.0.0.2 A\n")
    with open(log2, "w") as f:
        f.write("15 10.0.0.1 C\n20 10.0.0.1 A\n25 10.0.0.2 B\n")

    # The C program is hardcoded to write to /home/user/processed.log
    # Remove it first to ensure the program actually creates it
    if os.path.exists("/home/user/processed.log"):
        os.remove("/home/user/processed.log")

    # Run the program
    run_cmd = ["/tmp/log_processor_test", log1, log2]
    result = subprocess.run(run_cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Execution failed on hidden test case:\n{result.stderr}"

    # Verify output
    expected_hidden_output = """10 10.0.0.1 A
15 10.0.0.1 C
20 10.0.0.1 A
20 10.0.0.2 A
25 10.0.0.2 B
"""
    assert os.path.exists("/home/user/processed.log"), "processed.log was not created by the executable during the hidden test."
    with open("/home/user/processed.log", "r") as f:
        hidden_content = f.read()

    assert hidden_content == expected_hidden_output, f"Hidden test case output does not match expected logic. Expected:\n{expected_hidden_output}\nGot:\n{hidden_content}"