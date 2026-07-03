# test_final_state.py

import os
import re
import pytest

def test_debug_report_exists():
    report_path = "/home/user/debug_report.txt"
    assert os.path.exists(report_path), f"The debug report was not found at {report_path}."
    assert os.path.isfile(report_path), f"The path {report_path} is not a regular file."

def test_debug_report_content():
    report_path = "/home/user/debug_report.txt"
    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines() if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_path}, but found {len(lines)}."

    signature_line = lines[0]
    leak_line = lines[1]

    # Check signature line
    # Depending on the demangler, it might include the return type 'void' or not, 
    # and 'const double*' or 'double const*'.
    assert "process_record" in signature_line, "The function name 'process_record' is missing from the signature line."
    assert "double" in signature_line, "The type 'double' is missing from the signature line."
    assert "const" in signature_line, "The 'const' qualifier is missing from the signature line."
    assert "int" in signature_line, "The type 'int' is missing from the signature line."

    # Check leak line
    assert leak_line == "1024", f"Expected the memory leak to be exactly '1024' bytes, but got '{leak_line}'."