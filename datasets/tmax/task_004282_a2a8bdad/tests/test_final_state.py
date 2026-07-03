# test_final_state.py

import os
import re
import subprocess
import pytest

def test_crash_line_extracted():
    """Verify that the crash line was correctly extracted from the core dump."""
    crash_line_path = "/home/user/crash_line.txt"
    assert os.path.isfile(crash_line_path), f"File {crash_line_path} does not exist."

    with open(crash_line_path, "r") as f:
        content = f.read()

    expected_line = "2023-01-01 10:10:00|ERROR"
    assert content == expected_line, f"Expected crash line to be exactly '{expected_line}', but got '{content}'."

def test_makefile_fixed():
    """Verify that the legacy headers include path was removed from the Makefile."""
    makefile_path = "/home/user/log_processor/Makefile"
    assert os.path.isfile(makefile_path), f"File {makefile_path} does not exist."

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-I/home/user/legacy_headers" not in content, "Makefile still contains the conflicting legacy headers include path (-I/home/user/legacy_headers)."

def test_processor_c_null_check():
    """Verify that processor.c includes a null-check for the message variable."""
    source_path = "/home/user/log_processor/processor.c"
    assert os.path.isfile(source_path), f"File {source_path} does not exist."

    with open(source_path, "r") as f:
        content = f.read()

    # Look for common patterns of null checking the 'message' variable
    null_check_pattern = r'(!message|message\s*==\s*NULL|message\s*!=\s*NULL|message\s*&&|if\s*\(\s*message\s*\))'
    assert re.search(null_check_pattern, content), "Could not find a null-check for 'message' in processor.c before calling strlen."

def test_executable_runs_flawlessly():
    """Verify that the compiled executable exists and processes the log file without crashing."""
    exe_path = "/home/user/log_processor/log_processor"
    log_path = "/home/user/data/input.log"

    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist. Did you recompile?"
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

    # Run the executable against the input log
    result = subprocess.run([exe_path, log_path], capture_output=True, text=True)

    assert result.returncode == 0, f"log_processor failed with exit code {result.returncode}. Stderr: {result.stderr}"