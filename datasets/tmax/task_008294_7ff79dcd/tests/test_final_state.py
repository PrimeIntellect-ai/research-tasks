# test_final_state.py

import os
import re
import pytest

def test_alerts_sorted_txt():
    path = "/home/user/analyzer/alerts_sorted.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaUNIONSELECT",
        "/login.php?user=admin'UNION+SELECT+1,2,3--",
        "/search?q=UNION+SELECT+password+FROM+users"
    ]

    assert lines == expected_lines, f"Contents of {path} do not match the expected sorted, deduplicated output."

def test_parser_c_fixed():
    path = "/home/user/analyzer/parser.c"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Check that the unbounded sscanf is gone or fixed
    # Original was: sscanf(req, "GET %s HTTP", buf);
    # A safe one would have a length limit like %1023s, or use strncpy/strchr etc.
    unsafe_sscanf_pattern = r'sscanf\s*\([^,]+,\s*"[^"]*%s[^"]*"\s*,'
    assert not re.search(unsafe_sscanf_pattern, content), "parser.c still contains an unbounded sscanf with '%s'."

    # Also check for unbounded strcpy
    unsafe_strcpy_pattern = r'strcpy\s*\(\s*out\s*,\s*buf\s*\)'
    # If they still use a small buffer and strcpy, it might still be vulnerable if sscanf isn't bounded correctly, 
    # but the primary check is that they addressed the buffer overflow.
    # We will just ensure the obvious "%s" is removed or replaced.

def test_main_go_fixed():
    path = "/home/user/analyzer/main.go"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Look for evidence of synchronization: Mutex (Lock/Unlock) or Channels (<-)
    has_mutex = "Mutex" in content and ".Lock()" in content and ".Unlock()" in content
    has_channel = "chan " in content and "<-" in content
    has_sync_map = "sync.Map" in content

    assert has_mutex or has_channel or has_sync_map, "main.go does not appear to use synchronization (Mutex, Channel, or sync.Map) to fix the data race."

def test_binary_exists():
    path = "/home/user/analyzer/loganalyzer"
    assert os.path.isfile(path), f"Compiled binary {path} does not exist. Did you build the Go project?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."