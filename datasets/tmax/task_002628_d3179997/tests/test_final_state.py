# test_final_state.py
import os
import subprocess
import re

def test_crash_input_exists_and_format():
    """Verify that crash_input.txt exists and has the correct edge-case format."""
    crash_file = "/home/user/crash_input.txt"
    assert os.path.isfile(crash_file), f"Expected file {crash_file} does not exist."

    with open(crash_file, "r") as f:
        content = f.read()

    # The file should contain exactly one line (or at least the first line should trigger the bug)
    lines = content.splitlines()
    assert len(lines) >= 1, f"File {crash_file} is empty."
    first_line = lines[0]

    # The vulnerability is triggered when the message segment is empty.
    # Format: TIMESTAMP|SEVERITY|
    # The regex checks for two pipes and nothing (or just whitespace) after the second pipe.
    assert re.match(r'^[^|]*\|[^|]*\|$', first_line), \
        f"The content of {crash_file} does not match the expected edge-case format (e.g., 'TS|SEV|')."

def test_fixed_processor_source_exists():
    """Verify that the fixed source code exists."""
    source_file = "/home/user/fixed_processor.c"
    assert os.path.isfile(source_file), f"Expected source file {source_file} does not exist."

def test_fixed_processor_executable_exists():
    """Verify that the compiled fixed processor exists and is executable."""
    exe_file = "/home/user/fixed_processor"
    assert os.path.isfile(exe_file), f"Expected executable {exe_file} does not exist."
    assert os.access(exe_file, os.X_OK), f"File {exe_file} is not executable."

def test_fixed_processor_survives_crash_input():
    """Verify that the fixed processor does not crash when given the crash input."""
    exe_file = "/home/user/fixed_processor"
    crash_file = "/home/user/crash_input.txt"

    with open(crash_file, "r") as f:
        crash_data = f.read()

    try:
        result = subprocess.run(
            [exe_file],
            input=crash_data,
            text=True,
            capture_output=True,
            timeout=2
        )
    except subprocess.TimeoutExpired:
        assert False, "The fixed_processor timed out when processing the crash input."

    assert result.returncode == 0, f"The fixed_processor crashed or returned non-zero exit code: {result.returncode}"

def test_fixed_processor_normal_behavior():
    """Verify that the fixed processor still processes normal logs correctly."""
    exe_file = "/home/user/fixed_processor"
    normal_input = "TIME|WARN|Hello\n"
    expected_output = "PROCESSED: [WARN] Hello\n"

    try:
        result = subprocess.run(
            [exe_file],
            input=normal_input,
            text=True,
            capture_output=True,
            timeout=2
        )
    except subprocess.TimeoutExpired:
        assert False, "The fixed_processor timed out when processing normal input."

    assert result.returncode == 0, "The fixed_processor failed on normal input."
    assert result.stdout == expected_output, f"Expected output {repr(expected_output)}, got {repr(result.stdout)}"