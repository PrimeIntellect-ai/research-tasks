# test_final_state.py
import os
import sys

def test_logs_exist_and_passed():
    log_files = [
        "/home/user/test_pure_python.log",
        "/home/user/test_c_ext.log"
    ]
    for log_file in log_files:
        assert os.path.isfile(log_file), f"Log file {log_file} does not exist. Did you run the tests and redirect output?"
        with open(log_file, "r") as f:
            content = f.read()
        assert "2 passed" in content or "passed" in content.lower(), f"{log_file} does not indicate that tests passed successfully."

def test_setup_py_conditional():
    setup_path = "/home/user/fast-router/setup.py"
    assert os.path.isfile(setup_path), f"{setup_path} is missing."
    with open(setup_path, "r") as f:
        content = f.read()
    assert "PURE_PYTHON" in content, "setup.py does not contain conditional logic checking for 'PURE_PYTHON'."

def test_fetcher_patched():
    fetcher_path = "/home/user/fast-router/tests/test_fetcher.py"
    assert os.path.isfile(fetcher_path), f"{fetcher_path} is missing."
    with open(fetcher_path, "r") as f:
        content = f.read()
    assert "patch" in content, "tests/test_fetcher.py does not appear to use unittest.mock.patch."

def test_parser_fixes():
    sys.path.insert(0, "/home/user/fast-router")
    try:
        from router.parser import parse_routing_table
    except ImportError as e:
        assert False, f"Failed to import parse_routing_table: {e}"

    test_data = "PREFIX1 => DEST1\n\n# A comment line\nPREFIX2 => DEST2\n   \n#Another comment"
    try:
        result = parse_routing_table(test_data)
    except Exception as e:
        assert False, f"parse_routing_table crashed on valid input with empty lines and comments: {e}"

    expected = {"PREFIX1": "DEST1", "PREFIX2": "DEST2"}
    assert result == expected, f"parse_routing_table returned {result}, expected {expected}."