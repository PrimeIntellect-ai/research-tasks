# test_final_state.py
import os
import subprocess

def test_minimal_crash_bin_exists_and_size():
    minimal_bin_path = '/home/user/minimal_crash.bin'
    assert os.path.isfile(minimal_bin_path), f"Expected file {minimal_bin_path} does not exist."

    size = os.path.getsize(minimal_bin_path)
    assert size == 13, f"Expected minimal_crash.bin to be exactly 13 bytes, but got {size} bytes."

def test_crash_info_txt():
    crash_info_path = '/home/user/crash_info.txt'
    assert os.path.isfile(crash_info_path), f"Expected file {crash_info_path} does not exist."

    with open(crash_info_path, 'r') as f:
        content = f.read().strip()

    assert content == '13', f"Expected crash_info.txt to contain exactly '13', but got '{content}'."

def test_minimal_crash_triggers_exact_error():
    parser_path = '/home/user/parser.py'
    minimal_bin_path = '/home/user/minimal_crash.bin'

    assert os.path.isfile(parser_path), "parser.py is missing."
    assert os.path.isfile(minimal_bin_path), "minimal_crash.bin is missing."

    result = subprocess.run(
        ['python3', parser_path, minimal_bin_path],
        capture_output=True,
        text=True
    )

    # The script should crash (non-zero exit code)
    assert result.returncode != 0, "Expected parser.py to crash, but it exited normally."

    # The error message should be the specific struct.error
    expected_error = "struct.error: unpack requires a buffer of 8 bytes"
    assert expected_error in result.stderr, f"Expected stderr to contain '{expected_error}', but got:\n{result.stderr}"

def test_parser_unmodified():
    parser_path = '/home/user/parser.py'
    assert os.path.isfile(parser_path), "parser.py is missing."

    with open(parser_path, 'r') as f:
        content = f.read()

    assert "val = struct.unpack('<d', data[offset:offset+8])[0]" in content, "parser.py appears to have been modified."
    assert "if not data.startswith(b'MALW'):" in content, "parser.py appears to have been modified."