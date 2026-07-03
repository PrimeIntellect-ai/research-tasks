# test_final_state.py
import os
import time
import subprocess
import pytest

def test_scanner_compilation_and_execution():
    source_file = '/home/user/scanner.c'
    executable = '/home/user/scanner'
    output_hash_file = '/home/user/final_hash.txt'
    expected_hash_file = '/tmp/expected_hash.txt'

    assert os.path.isfile(source_file), f"Source file {source_file} does not exist."
    assert os.path.isfile(expected_hash_file), f"Expected hash file {expected_hash_file} is missing."

    # Check for seccomp usage in source code
    with open(source_file, 'r') as f:
        source_code = f.read()

    assert "seccomp" in source_code, "The source code must use seccomp for process isolation."
    assert "execve" in source_code, "The seccomp filter must explicitly deny 'execve'."
    assert "socket" in source_code, "The seccomp filter must explicitly deny 'socket'."
    assert "connect" in source_code, "The seccomp filter must explicitly deny 'connect'."

    # Compile the C program
    compile_proc = subprocess.run(
        ['gcc', '-O3', source_file, '-lssl', '-lcrypto', '-lseccomp', '-o', executable],
        capture_output=True,
        text=True
    )
    assert compile_proc.returncode == 0, f"Compilation failed:\n{compile_proc.stderr}"

    # Remove the output file if it exists from previous runs
    if os.path.exists(output_hash_file):
        os.remove(output_hash_file)

    # Execute and measure runtime
    start_time = time.time()
    run_proc = subprocess.run([executable], capture_output=True, text=True)
    end_time = time.time()

    assert run_proc.returncode == 0, f"Execution failed with return code {run_proc.returncode}:\n{run_proc.stderr}"

    runtime = end_time - start_time

    # Verify the output hash
    assert os.path.isfile(output_hash_file), f"Output file {output_hash_file} was not created."

    with open(output_hash_file, 'r') as f:
        agent_hash = f.read().strip()

    with open(expected_hash_file, 'r') as f:
        expected_hash = f.read().strip()

    assert agent_hash == expected_hash, f"Hash mismatch. Expected {expected_hash}, got {agent_hash}."

    # Assert performance constraint
    threshold = 0.25
    assert runtime <= threshold, f"Execution time {runtime:.4f}s exceeded the threshold of {threshold}s."