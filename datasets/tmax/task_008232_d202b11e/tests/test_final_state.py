# test_final_state.py

import os
import subprocess
import re

WORKSPACE = '/home/user/workspace'

def test_libtoken_so_exists():
    lib_path = os.path.join(WORKSPACE, 'libtoken.so')
    assert os.path.isfile(lib_path), f"Shared library {lib_path} does not exist. Did you compile token_parser.c?"

def test_test_report_exists_and_passed():
    report_path = os.path.join(WORKSPACE, 'test_report.txt')
    assert os.path.isfile(report_path), f"Test report {report_path} does not exist."

    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "OK" in content, f"Test report does not indicate success (missing 'OK'). Content:\n{content}"
    assert re.search(r"Ran 2 tests", content), "Test report does not indicate that 2 tests were run."

def test_security_tool_fixes():
    script_path = os.path.join(WORKSPACE, 'security_tool.py')
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert "argtypes" in content, "Missing 'argtypes' configuration in security_tool.py"
    assert "restype" in content, "Missing 'restype' configuration in security_tool.py"
    assert "create_string_buffer" in content, "Missing 'ctypes.create_string_buffer' in security_tool.py to safely pass mutable string."

def test_mock_fixture_fixes():
    test_script_path = os.path.join(WORKSPACE, 'test_security_tool.py')
    assert os.path.isfile(test_script_path), f"{test_script_path} does not exist."

    with open(test_script_path, 'r', encoding='utf-8') as f:
        content = f.read()

    assert 'read_data=b"TOKEN' in content or "read_data=b'TOKEN" in content, "mock_open read_data must be updated to return bytes (e.g., b'TOKEN...')."

def test_run_test_suite_passes():
    # Verify that the test suite actually passes now
    result = subprocess.run(
        ['python3', '-m', 'unittest', 'test_security_tool.py'],
        cwd=WORKSPACE,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Test suite still fails when run. stdout:\n{result.stdout}\nstderr:\n{result.stderr}"