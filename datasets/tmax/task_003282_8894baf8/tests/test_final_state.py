# test_final_state.py

import os
import subprocess
import pytest

MINIMAL_CRASH_FILE = "/home/user/minimal_crash.bin"
PROCESSOR_FIXED_C = "/home/user/processor_fixed.c"
ORIGINAL_PROCESSOR = "/home/user/processor"

def test_minimal_crash_exists():
    assert os.path.isfile(MINIMAL_CRASH_FILE), f"Missing minimal crash payload: {MINIMAL_CRASH_FILE}"

def test_minimal_crash_causes_segfault():
    # Run the original processor with the minimal crash payload
    result = subprocess.run(
        [ORIGINAL_PROCESSOR, MINIMAL_CRASH_FILE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    # Segfault usually results in returncode -11 (SIGSEGV) or 139 (128 + 11)
    assert result.returncode in (-11, 139), f"Expected {MINIMAL_CRASH_FILE} to cause a segfault, but got return code {result.returncode}"

def test_minimal_crash_is_minimized():
    with open(MINIMAL_CRASH_FILE, "rb") as f:
        crash_data = f.read()

    # If we remove 1 byte, it should NOT crash
    if len(crash_data) > 0:
        smaller_payload = crash_data[:-1]
        test_file = "/tmp/test_smaller_payload.bin"
        with open(test_file, "wb") as f:
            f.write(smaller_payload)

        result = subprocess.run(
            [ORIGINAL_PROCESSOR, test_file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        os.remove(test_file)

        assert result.returncode not in (-11, 139), f"Payload is not minimized. A payload of length {len(smaller_payload)} still causes a crash."

def test_processor_fixed_exists_and_compiles():
    assert os.path.isfile(PROCESSOR_FIXED_C), f"Missing fixed source code: {PROCESSOR_FIXED_C}"

    compile_result = subprocess.run(
        ["gcc", "-g", "-fno-stack-protector", "-O0", PROCESSOR_FIXED_C, "-o", "/tmp/processor_fixed"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    assert compile_result.returncode == 0, f"Failed to compile {PROCESSOR_FIXED_C}:\n{compile_result.stderr.decode()}"

def test_processor_fixed_does_not_crash():
    # Ensure it's compiled
    if not os.path.isfile("/tmp/processor_fixed"):
        pytest.skip("Fixed processor binary not found, compilation probably failed.")

    result = subprocess.run(
        ["/tmp/processor_fixed", MINIMAL_CRASH_FILE],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    assert result.returncode not in (-11, 139), f"Fixed processor still crashes on {MINIMAL_CRASH_FILE}"