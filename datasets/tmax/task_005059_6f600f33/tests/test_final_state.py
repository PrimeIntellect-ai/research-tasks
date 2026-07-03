# test_final_state.py

import os
import re
import stat
import pytest

PROJECT_DIR = "/home/user/polyglot_calc"
BUILD_SCRIPT = os.path.join(PROJECT_DIR, "build_and_test.sh")
CLIENT_OUTPUT = "/home/user/client_output.txt"
VALGRIND_REPORT = "/home/user/valgrind_report.txt"

def test_build_script_exists_and_executable():
    assert os.path.isfile(BUILD_SCRIPT), f"Build script {BUILD_SCRIPT} does not exist."
    st = os.stat(BUILD_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Build script {BUILD_SCRIPT} is not executable."

def test_client_output_correct():
    assert os.path.isfile(CLIENT_OUTPUT), f"Client output file {CLIENT_OUTPUT} does not exist. Did the build_and_test.sh script run and generate it?"

    with open(CLIENT_OUTPUT, "r", encoding="utf-8") as f:
        content = f.read()

    # The expected evaluation of "3 4 + 5 *" is 35.
    # The client output should contain "35"
    assert "35" in content, f"Expected to find '35' in {CLIENT_OUTPUT}, but got:\n{content}"

def test_valgrind_report_no_leaks():
    assert os.path.isfile(VALGRIND_REPORT), f"Valgrind report {VALGRIND_REPORT} does not exist. Did the build_and_test.sh script run the server under valgrind?"

    with open(VALGRIND_REPORT, "r", encoding="utf-8") as f:
        content = f.read()

    # Look for "definitely lost: 0 bytes in 0 blocks"
    # Valgrind output might have formatting, e.g., "definitely lost: 0 bytes in 0 blocks"
    match = re.search(r"definitely lost:\s*0 bytes in 0 blocks", content, re.IGNORECASE)
    assert match is not None, f"Memory leak detected or valgrind report incomplete. Expected 'definitely lost: 0 bytes in 0 blocks' in {VALGRIND_REPORT}. Content:\n{content}"

def test_cpp_evaluator_fixed():
    evaluator_file = os.path.join(PROJECT_DIR, "cpp_server", "evaluator.cc")
    assert os.path.isfile(evaluator_file), f"evaluator.cc {evaluator_file} is missing."

    with open(evaluator_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Check that the logic bug is fixed (should be * instead of + for multiplication)
    # The original buggy line was: if (token == "*") *res = *a + *b;
    assert re.search(r'\*\s*a\s*\*\s*\*\s*b', content) or re.search(r'\*\s*b\s*\*\s*\*\s*a', content) or "a * b" in content.replace("*a", "a").replace("*b", "b"), "The multiplication logic bug in evaluator.cc does not appear to be fixed."