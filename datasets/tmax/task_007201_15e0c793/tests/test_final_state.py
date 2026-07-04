# test_final_state.py

import os
import sys
import pytest
import importlib

def test_parser_c_fixed():
    file_path = "/home/user/waf_pipeline/parser.c"
    assert os.path.isfile(file_path), f"{file_path} is missing."
    with open(file_path, "r") as f:
        content = f.read()
    assert "strcpy(buffer, input);" not in content, "parser.c still contains the strcpy vulnerability."
    assert "strncpy" in content or "snprintf" in content or "strlcpy" in content or "PyArg_ParseTuple(args, \"s#\", &input, &length)" in content, "parser.c does not seem to use a safe string copy function."

def test_setup_py_exists():
    file_path = "/home/user/waf_pipeline/setup.py"
    assert os.path.isfile(file_path), f"{file_path} is missing. setup.py was not created."

def test_waf_parser_importable():
    # Add the directory to sys.path just in case it was built in place but not installed cleanly,
    # though the instructions said `pip install -e .`.
    sys.path.insert(0, "/home/user/waf_pipeline")
    try:
        import waf_parser
    except ImportError as e:
        pytest.fail(f"Could not import waf_parser. Ensure it was compiled and installed. Error: {e}")

    assert hasattr(waf_parser, "extract_payload"), "waf_parser is missing the extract_payload function."

    # Test that it safely handles large strings without segfaulting
    large_string = "A" * 300
    try:
        result = waf_parser.extract_payload(large_string)
        # As long as it doesn't crash, it passes.
        assert isinstance(result, str), "extract_payload should return a string."
    except Exception as e:
        pytest.fail(f"extract_payload raised an exception on large input: {e}")

def test_blocked_log_correct():
    file_path = "/home/user/waf_pipeline/blocked.log"
    assert os.path.isfile(file_path), f"{file_path} is missing. WAF script might not have run or failed to produce output."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "[BLOCKED] admin'-- IN GET /login?user=admin'-- HTTP/1.1",
        "[BLOCKED] <script> IN POST /submit?data=<script>alert(1)</script> HTTP/1.1",
        "[BLOCKED] DROP TABLE IN GET /api/data?query=SELECT * FROM users; DROP TABLE users; HTTP/1.1",
        "[BLOCKED] /etc/passwd IN GET /home?file=../../../../etc/passwd HTTP/1.1"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} blocked payloads, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} mismatch.\nExpected: {expected}\nActual: {actual}"

def test_run_waf_py_exists():
    file_path = "/home/user/waf_pipeline/run_waf.py"
    assert os.path.isfile(file_path), f"{file_path} is missing."