# test_final_state.py

import os
import time
import subprocess
import stat

def test_fast_parser_runtime_and_output():
    executable = "/home/user/fast_parser"
    assert os.path.isfile(executable), f"Executable {executable} not found."
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

    output_file = "/home/user/output.pack"
    if os.path.exists(output_file):
        os.remove(output_file)

    start_time = time.time()
    result = subprocess.run([executable], capture_output=True)
    end_time = time.time()

    assert result.returncode == 0, f"Execution failed with return code {result.returncode}.\nstdout: {result.stdout.decode()}\nstderr: {result.stderr.decode()}"

    runtime = end_time - start_time
    assert runtime <= 1.5, f"Runtime {runtime:.4f}s exceeded the 1.5s threshold."

    assert os.path.isfile(output_file), f"Output file {output_file} was not created."
    assert os.path.getsize(output_file) > 0, f"Output file {output_file} is empty."

def test_fixed_library_exists():
    library = "/app/libdata-packer-1.0/libdatapacker.a"
    assert os.path.isfile(library), f"Static library {library} not found. Did you compile the fixed library?"

def test_parser_source_exists():
    source = "/home/user/parser.cpp"
    assert os.path.isfile(source), f"Source file {source} not found."