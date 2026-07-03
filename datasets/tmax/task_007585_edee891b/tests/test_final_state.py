# test_final_state.py

import os
import pytest

OUTPUT_FILE = "/home/user/charlie_permissions.txt"
C_SOURCE_FILE = "/home/user/audit_resolver.c"
BINARY_FILE = "/home/user/audit_resolver"

EXPECTED_PERMISSIONS = [
    "EXPORT_AUDIT_LOGS",
    "INTERNAL_LOGIN",
    "READ_WIKI",
    "VIEW_FINANCIALS",
    "VIEW_PUBLIC_PAGES"
]

def test_source_and_binary_exist():
    """Verify that the C source code and compiled binary exist."""
    assert os.path.isfile(C_SOURCE_FILE), f"C source file not found at {C_SOURCE_FILE}"
    assert os.path.isfile(BINARY_FILE), f"Compiled binary not found at {BINARY_FILE}"
    assert os.access(BINARY_FILE, os.X_OK), f"Compiled file at {BINARY_FILE} is not executable"

def test_output_file_exists_and_correct():
    """Verify that the output file exists and contains the correct resolved permissions."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert lines == EXPECTED_PERMISSIONS, (
        f"Output file contents do not match expected permissions.\n"
        f"Expected: {EXPECTED_PERMISSIONS}\n"
        f"Found: {lines}"
    )