# test_final_state.py

import os
import random
import string
import subprocess
import pytest

def test_build_system_fixed():
    work_dir = "/home/user/pipeline_tools"

    # Ensure the directory exists
    assert os.path.isdir(work_dir), f"Directory not found: {work_dir}"

    # Run make clean
    subprocess.run(["make", "clean"], cwd=work_dir, capture_output=True)

    # Run make
    make_result = subprocess.run(["make"], cwd=work_dir, capture_output=True, text=True)
    assert make_result.returncode == 0, f"make failed with error:\n{make_result.stderr}"

    # Check if expected files were created
    expected_files = ["libalpha.so", "libbeta.so", "pipeline_test"]
    for f in expected_files:
        file_path = os.path.join(work_dir, f)
        assert os.path.isfile(file_path), f"Expected build artifact missing: {f}"

    # Run the pipeline_test executable
    env = os.environ.copy()
    env["LD_LIBRARY_PATH"] = work_dir + ":" + env.get("LD_LIBRARY_PATH", "")
    test_result = subprocess.run(["./pipeline_test"], cwd=work_dir, env=env, capture_output=True, text=True)
    assert test_result.returncode == 0, f"pipeline_test failed to run:\n{test_result.stderr}"

def test_stream_processor_fuzz_equivalence():
    agent_path = "/home/user/stream_processor"
    oracle_path = "/app/oracle_processor"

    assert os.path.isfile(agent_path), f"Agent stream processor not found at {agent_path}"
    assert os.access(agent_path, os.X_OK), f"Agent stream processor at {agent_path} is not executable"

    assert os.path.isfile(oracle_path), f"Oracle stream processor not found at {oracle_path}"
    assert os.access(oracle_path, os.X_OK), f"Oracle stream processor at {oracle_path} is not executable"

    # Fuzz Distribution: random strings. Length uniformly distributed between 0 and 5000 characters.
    # Character set includes alphanumeric ASCII, spaces, newlines, `<`, `>`, `&`, and `` ` ``.
    char_set = string.ascii_letters + string.digits + " \n<>&`"

    # We will test 100 random strings to keep the test execution time reasonable, 
    # but still rigorous enough to catch edge cases.
    num_tests = 100
    random.seed(42)

    for i in range(num_tests):
        length = random.randint(0, 5000)
        test_input = "".join(random.choice(char_set) for _ in range(length))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_path],
            input=test_input,
            capture_output=True,
            text=True
        )
        assert oracle_proc.returncode == 0, f"Oracle failed on input length {length}"
        oracle_output = oracle_proc.stdout

        # Run agent
        agent_proc = subprocess.run(
            [agent_path],
            input=test_input,
            capture_output=True,
            text=True
        )

        assert agent_proc.returncode == 0, f"Agent failed on input length {length}. Stderr: {agent_proc.stderr}"
        agent_output = agent_proc.stdout

        if agent_output != oracle_output:
            # Truncate input/output for display if they are too long
            display_input = test_input if len(test_input) <= 200 else test_input[:200] + "... [truncated]"
            display_oracle = oracle_output if len(oracle_output) <= 200 else oracle_output[:200] + "... [truncated]"
            display_agent = agent_output if len(agent_output) <= 200 else agent_output[:200] + "... [truncated]"

            error_msg = (
                f"Mismatch found on fuzz test {i+1}/{num_tests}.\n"
                f"Input:\n{display_input}\n\n"
                f"Expected (Oracle):\n{display_oracle}\n\n"
                f"Got (Agent):\n{display_agent}"
            )
            pytest.fail(error_msg)