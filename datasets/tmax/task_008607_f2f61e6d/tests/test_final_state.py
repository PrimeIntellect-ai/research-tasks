# test_final_state.py
import os
import subprocess
import pytest

def test_minimized_bin_crashes_original():
    min_bin = "/home/user/minimized.bin"
    assert os.path.isfile(min_bin), "minimized.bin not found at /home/user/minimized.bin"

    # Check if it's reasonably small
    size = os.path.getsize(min_bin)
    assert size <= 50, f"minimized.bin is too large ({size} bytes) to be minimal."

    orig_c = "/home/user/log_ingestor.c"
    orig_bin = "/tmp/log_ingestor_orig"

    # Compile original code to test the crash
    compile_res = subprocess.run(["gcc", orig_c, "-o", orig_bin], capture_output=True)
    assert compile_res.returncode == 0, "Failed to compile the original log_ingestor.c"

    out_file = "/tmp/out_minimized.bin"
    result = subprocess.run([orig_bin, min_bin, out_file], capture_output=True)

    # A crash should result in a non-zero return code (typically a negative signal number or > 128)
    assert result.returncode != 0, "minimized.bin did not cause the original binary to crash."

def test_fixed_binary_handles_crash_bin():
    fixed_bin = "/home/user/log_ingestor_fixed"
    assert os.path.isfile(fixed_bin), "Fixed binary not found at /home/user/log_ingestor_fixed"
    assert os.access(fixed_bin, os.X_OK), "Fixed binary is not executable"

    crash_bin = "/home/user/crash.bin"
    out_file = "/tmp/out_fixed.bin"

    # Ensure any previous output is removed
    if os.path.exists(out_file):
        os.remove(out_file)

    result = subprocess.run([fixed_bin, crash_bin, out_file], capture_output=True)
    assert result.returncode == 0, "Fixed binary crashed or failed when processing crash.bin"

    assert os.path.isfile(out_file), "Fixed binary did not produce output for crash.bin"

    with open(out_file, "rb") as f:
        content = f.read()

    # The requirement is to cap the decoded output to exactly fill the 1024-byte buffer
    assert len(content) == 1024, f"Expected output length to be capped at exactly 1024 bytes, got {len(content)} bytes."
    assert all(b == 0xaa for b in content), "Decoded output content does not match the expected payload."

def test_data_fixed_bin_content():
    data_fixed = "/home/user/data_fixed.bin"
    assert os.path.isfile(data_fixed), "data_fixed.bin not found at /home/user/data_fixed.bin"

    with open(data_fixed, "rb") as f:
        content = f.read()

    expected = b"\x01\x04\x04\x03\x02\x01"
    assert content == expected, f"data_fixed.bin content mismatch. Expected {expected}, got {content}"

def test_fixed_code_exists():
    fixed_c = "/home/user/log_ingestor_fixed.c"
    assert os.path.isfile(fixed_c), f"Fixed source code not found at {fixed_c}"