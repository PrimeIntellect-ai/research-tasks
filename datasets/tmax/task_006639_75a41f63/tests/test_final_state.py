# test_final_state.py

import os
import subprocess
import re
import pytest

PIPELINE_DIR = "/home/user/pipeline"
RUN_PIPELINE = os.path.join(PIPELINE_DIR, "run_pipeline.sh")
TEST_PIPELINE = os.path.join(PIPELINE_DIR, "test_pipeline.sh")
PROCESSOR_JS = os.path.join(PIPELINE_DIR, "processor.js")
INGESTER_PY = os.path.join(PIPELINE_DIR, "ingester.py")

def test_test_pipeline_script_exists_and_executable():
    assert os.path.isfile(TEST_PIPELINE), f"Regression test script {TEST_PIPELINE} is missing."
    assert os.access(TEST_PIPELINE, os.X_OK), f"Regression test script {TEST_PIPELINE} is not executable."

def test_test_pipeline_script_succeeds():
    # Run the regression test script
    result = subprocess.run([TEST_PIPELINE], capture_output=True, text=True)
    assert result.returncode == 0, f"{TEST_PIPELINE} failed with exit code {result.returncode}. Output: {result.stdout} {result.stderr}"

def test_run_pipeline_env_var_configured():
    with open(RUN_PIPELINE, 'r') as f:
        content = f.read()
    assert "PIPELINE_MODE=production" in content, f"{RUN_PIPELINE} does not set PIPELINE_MODE=production."

def test_run_pipeline_output_success():
    result = subprocess.run([RUN_PIPELINE], capture_output=True, text=True)
    assert result.returncode == 0, f"{RUN_PIPELINE} failed to execute properly."
    assert "SUCCESS: critical" in result.stdout, f"Expected output 'SUCCESS: critical' not found in {RUN_PIPELINE} output."

def test_processor_js_infinite_recursion_fixed():
    # To test if infinite recursion is fixed, we can run the processor with the legacy output.
    # It should exit with an error rather than hanging (which would cause a timeout).
    env = os.environ.copy()
    env["PIPELINE_MODE"] = "legacy"

    try:
        # Run ingester piped to processor
        p1 = subprocess.Popen(["python3", INGESTER_PY], stdout=subprocess.PIPE, env=env)
        p2 = subprocess.Popen(["node", PROCESSOR_JS], stdin=p1.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        p1.stdout.close()

        # If it's not fixed, it will hang or hit stack size limit (which might take a bit or throw RangeError).
        # We enforce a timeout of 3 seconds.
        stdout, stderr = p2.communicate(timeout=3)

        # It should fail with an error, not succeed, because legacy output has a trailing comma in an array
        # which the resilientParse doesn't fix.
        assert p2.returncode != 0, "Processor should fail when parsing legacy output, but it succeeded."

    except subprocess.TimeoutExpired:
        p2.kill()
        pytest.fail("processor.js timed out, indicating the infinite recursion bug is not fixed.")