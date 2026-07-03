# test_final_state.py
import os
import subprocess
import pytest

RATIONAL_SCRIPT = "/home/user/rational.sh"
TEST_SCRIPT = "/home/user/test_rational.sh"
TEST_LOG = "/home/user/test_result.log"

def run_bash_function(script_path, func_name, *args):
    """Sources the script and runs the specified function with arguments."""
    args_str = " ".join(map(str, args))
    cmd = f"source {script_path} && {func_name} {args_str}"
    result = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True)
    return result.stdout.strip(), result.returncode

def test_scripts_exist():
    assert os.path.isfile(RATIONAL_SCRIPT), f"{RATIONAL_SCRIPT} is missing."
    assert os.path.isfile(TEST_SCRIPT), f"{TEST_SCRIPT} is missing."

def test_add_rat_logic():
    assert os.path.isfile(RATIONAL_SCRIPT), f"{RATIONAL_SCRIPT} is missing."

    test_cases = [
        ((1, 4, 1, 4), "1/2"),
        ((-1, 3, 1, -2), "-5/6"),
        ((0, 5, 0, 8), "0/1"),
        ((1, 3, 1, 3), "2/3"),
        ((5, 2, -5, 2), "0/1"),
        ((-3, -4, -1, -4), "1/1")
    ]

    for args, expected in test_cases:
        out, rc = run_bash_function(RATIONAL_SCRIPT, "add_rat", *args)
        assert rc == 0, f"add_rat failed with return code {rc} for args {args}"
        assert out == expected, f"add_rat {args} returned '{out}', expected '{expected}'"

def test_mul_rat_logic():
    assert os.path.isfile(RATIONAL_SCRIPT), f"{RATIONAL_SCRIPT} is missing."

    test_cases = [
        ((-2, 3, 6, 5), "-4/5"),
        ((-1, -2, -3, -4), "1/8"),
        ((5, 1, 0, 2), "0/1"),
        ((3, 4, 4, 3), "1/1"),
        ((-1, 2, 2, 1), "-1/1")
    ]

    for args, expected in test_cases:
        out, rc = run_bash_function(RATIONAL_SCRIPT, "mul_rat", *args)
        assert rc == 0, f"mul_rat failed with return code {rc} for args {args}"
        assert out == expected, f"mul_rat {args} returned '{out}', expected '{expected}'"

def test_no_external_binaries():
    assert os.path.isfile(RATIONAL_SCRIPT), f"{RATIONAL_SCRIPT} is missing."
    with open(RATIONAL_SCRIPT, "r") as f:
        content = f.read()

    forbidden = ["bc", "awk", "python", "perl", "ruby", "node"]
    for word in forbidden:
        # A rudimentary check to ensure they are not relying on obvious external tools
        assert word not in content.split(), f"Forbidden external tool '{word}' found in {RATIONAL_SCRIPT}"

def test_test_script_execution():
    assert os.path.isfile(TEST_SCRIPT), f"{TEST_SCRIPT} is missing."

    # Remove log if exists from previous manual runs
    if os.path.exists(TEST_LOG):
        os.remove(TEST_LOG)

    result = subprocess.run(["bash", TEST_SCRIPT], capture_output=True, text=True)
    assert result.returncode == 0, f"{TEST_SCRIPT} failed with return code {result.returncode}. stderr: {result.stderr}"

    assert os.path.isfile(TEST_LOG), f"{TEST_LOG} was not created by the test script."
    with open(TEST_LOG, "r") as f:
        log_content = f.read().strip()
    assert log_content == "ALL_PASS", f"Expected '{TEST_LOG}' to contain 'ALL_PASS', but got '{log_content}'"

def test_test_script_contents():
    assert os.path.isfile(TEST_SCRIPT), f"{TEST_SCRIPT} is missing."
    with open(TEST_SCRIPT, "r") as f:
        content = f.read()

    assert "add_rat" in content, f"{TEST_SCRIPT} does not invoke add_rat."
    assert "for " in content or "while " in content, f"{TEST_SCRIPT} does not appear to contain a loop."