# test_final_state.py
import os
import subprocess
import tempfile
import textwrap

def test_files_exist():
    """Verify that the required files exist."""
    assert os.path.exists("/home/user/libfetch.so"), "/home/user/libfetch.so is missing"
    assert os.path.exists("/home/user/build_pipeline.py"), "/home/user/build_pipeline.py is missing"
    assert os.path.exists("/home/user/pipeline.log"), "/home/user/pipeline.log is missing"

def test_pipeline_log_contents():
    """Verify the contents of the pipeline.log file."""
    expected_lines = [
        "URL: https://internal.build.corp/asset1.zip, Status: 0, Output: https://internal.build.corp/asset1.zip",
        "URL: https://internal%2Ebuild%2Ecorp/asset2.zip, Status: 0, Output: https://internal.build.corp/asset2.zip",
        "URL: https://external.com/%2E%2E/internal.build.corp/, Status: -1, Output: ",
        "URL: https://internal.build.corp/asset3.zip, Status: -2, Output: ",
        "URL: https://internal.build.corp/asset4.zip, Status: -2, Output: "
    ]

    with open("/home/user/pipeline.log", "r") as f:
        actual_lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in pipeline.log, got {len(actual_lines)}"

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual: {actual}"

def test_libfetch_behavior():
    """Verify libfetch.so behavior in an isolated process to test rate limiting and decoding."""
    test_script = textwrap.dedent("""
    import ctypes
    import sys

    try:
        lib = ctypes.CDLL("/home/user/libfetch.so")
    except Exception as e:
        print(f"Failed to load library: {e}")
        sys.exit(10)

    lib.validate_and_fetch.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    lib.validate_and_fetch.restype = ctypes.c_int

    buf = ctypes.create_string_buffer(256)

    # Call 1: complex payload decoding check
    url1 = b"%68%74%74%70%73%3A%2F%2F%69%6E%74%65%72%6E%61%6C%2E%62%75%69%6C%64%2E%63%6F%72%70%2F%74%65%73%74"
    res1 = lib.validate_and_fetch(url1, buf)
    if res1 != 0:
        print(f"Call 1 failed with status {res1}")
        sys.exit(1)
    if buf.value != b"https://internal.build.corp/test":
        print(f"Call 1 decoded output incorrect: {buf.value}")
        sys.exit(2)

    # Call 2: valid
    res2 = lib.validate_and_fetch(b"https://internal.build.corp/2", buf)
    if res2 != 0:
        print(f"Call 2 failed with status {res2}")
        sys.exit(3)

    # Call 3: valid
    res3 = lib.validate_and_fetch(b"https://internal.build.corp/3", buf)
    if res3 != 0:
        print(f"Call 3 failed with status {res3}")
        sys.exit(4)

    # Call 4: rate limit expected
    res4 = lib.validate_and_fetch(b"https://internal.build.corp/4", buf)
    if res4 != -2:
        print(f"Call 4 rate limit failed, got status {res4} instead of -2")
        sys.exit(5)

    sys.exit(0)
    """)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        script_path = f.name

    try:
        result = subprocess.run(["python3", script_path], capture_output=True, text=True)
        assert result.returncode == 0, f"libfetch.so behavior test failed: {result.stdout}\n{result.stderr}"
    finally:
        os.remove(script_path)