# test_final_state.py

import os
import subprocess
import pytest

WORKSPACE_DIR = "/home/user/polyglot_math"

def test_makefile_repaired():
    makefile_path = os.path.join(WORKSPACE_DIR, "Makefile")
    assert os.path.isfile(makefile_path), f"Makefile is missing at {makefile_path}"

    with open(makefile_path, "r") as f:
        content = f.read()

    assert "-lm" in content, "Makefile does not contain '-lm' for linking the math library."

    # Check for tabs instead of spaces in the command lines
    lines = content.split('\n')
    has_tab_rule = False
    for line in lines:
        if line.strip().startswith("$(CC)") or line.strip().startswith("rm -f"):
            assert line.startswith("\t"), f"Makefile command '{line.strip()}' must start with a tab character, not spaces."
            has_tab_rule = True

    assert has_tab_rule, "Could not find compile or clean rules in the Makefile to verify tabs."

def test_collatz_py_exists_and_works():
    collatz_py = os.path.join(WORKSPACE_DIR, "collatz.py")
    assert os.path.isfile(collatz_py), f"{collatz_py} is missing."

    # Test collatz.py logic with some sample inputs
    input_data = "5\n13\n"
    proc = subprocess.run(
        ["python3", collatz_py],
        input=input_data,
        text=True,
        capture_output=True
    )
    assert proc.returncode == 0, f"collatz.py failed to run. Stderr: {proc.stderr}"
    output = proc.stdout.strip().split('\n')
    assert "5,5" in output, "collatz.py did not output correctly for input 5."
    assert "13,9" in output, "collatz.py did not output correctly for input 13."

def test_pipeline_py_execution():
    pipeline_py = os.path.join(WORKSPACE_DIR, "pipeline.py")
    assert os.path.isfile(pipeline_py), f"{pipeline_py} is missing."

    # Run pipeline.py
    proc = subprocess.run(
        ["python3", pipeline_py],
        cwd=WORKSPACE_DIR,
        capture_output=True,
        text=True
    )

    assert proc.returncode == 0, f"pipeline.py exited with code {proc.returncode}. Stderr: {proc.stderr}\nStdout: {proc.stdout}"
    assert "PIPELINE SUCCESS" in proc.stdout, "pipeline.py did not print 'PIPELINE SUCCESS' to standard output."

    pipeline_output = os.path.join(WORKSPACE_DIR, "pipeline_output.txt")
    expected_output = os.path.join(WORKSPACE_DIR, "expected_output.txt")

    assert os.path.isfile(pipeline_output), f"{pipeline_output} was not created by the pipeline."

    with open(pipeline_output, "r") as f1, open(expected_output, "r") as f2:
        pipeline_content = f1.read().strip()
        expected_content = f2.read().strip()

    assert pipeline_content == expected_content, "The contents of pipeline_output.txt do not match expected_output.txt."