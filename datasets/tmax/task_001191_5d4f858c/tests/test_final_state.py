# test_final_state.py

import os
import stat
import string
import random
import subprocess
import pytest

AGENT_SCRIPT = "/home/user/filter_script.py"
ORACLE_SCRIPT = "/verify/oracle_filter.py"

def test_script_exists_and_executable():
    assert os.path.isfile(AGENT_SCRIPT), f"Agent script not found at {AGENT_SCRIPT}"
    st = os.stat(AGENT_SCRIPT)
    assert bool(st.st_mode & stat.S_IXUSR), f"Agent script {AGENT_SCRIPT} is not executable"

def generate_random_line():
    length = random.randint(5, 1000)
    chars = string.ascii_letters + string.digits + string.punctuation + " "
    return "".join(random.choices(chars, k=length))

def test_fuzz_equivalence():
    random.seed(42)

    # Generate 10 test cases, each with 100 lines
    num_test_cases = 10
    lines_per_case = 100

    for i in range(num_test_cases):
        input_lines = [generate_random_line() for _ in range(lines_per_case)]
        input_text = "\n".join(input_lines) + "\n"

        # Run oracle
        oracle_proc = subprocess.run(
            [ORACLE_SCRIPT],
            input=input_text,
            text=True,
            capture_output=True,
            check=True
        )
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [AGENT_SCRIPT],
            input=input_text,
            text=True,
            capture_output=True
        )

        assert agent_proc.returncode == 0, f"Agent script failed with error:\n{agent_proc.stderr}"

        agent_output = agent_proc.stdout

        if agent_output != oracle_output:
            pytest.fail(
                f"Output mismatch on test case {i+1}.\n"
                f"--- Oracle Output ---\n{oracle_output[:500]}\n"
                f"--- Agent Output ---\n{agent_output[:500]}\n"
            )

def test_fasttext_installed():
    # Verify that fasttext can be imported in the current environment
    try:
        import fasttext
    except ImportError:
        pytest.fail("fasttext module is not installed in the Python environment.")