# test_final_state.py

import os
import subprocess
import pytest

PROJ_DIR = "/home/user/pipeline_proj"
RESULTS_LOG = "/home/user/test_results.log"
TRANSFORMER_RS = os.path.join(PROJ_DIR, "src", "transformer.rs")

def test_test_results_log_success():
    """Verify that the test_results.log file exists and contains exactly SUCCESS."""
    assert os.path.isfile(RESULTS_LOG), f"{RESULTS_LOG} does not exist. Did you run the e2e script?"

    with open(RESULTS_LOG, "r") as f:
        content = f.read()

    assert content == "SUCCESS\n", f"Expected exactly 'SUCCESS\\n' in {RESULTS_LOG}, but got {repr(content)}"

def test_rust_project_compiles():
    """Verify that the Rust project compiles successfully without errors."""
    assert os.path.isdir(PROJ_DIR), f"{PROJ_DIR} does not exist."

    # Run cargo check to verify compilation
    result = subprocess.run(
        ["cargo", "check"],
        cwd=PROJ_DIR,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"cargo check failed in {PROJ_DIR}:\n{result.stderr}"

def test_transformer_rs_fixed():
    """Verify that transformer.rs was updated to use String instead of &str."""
    assert os.path.isfile(TRANSFORMER_RS), f"{TRANSFORMER_RS} is missing."

    with open(TRANSFORMER_RS, "r") as f:
        content = f.read()

    assert "Vec<String>" in content, f"Expected return type Vec<String> in {TRANSFORMER_RS}, but it was not found."
    assert "result.push(upper.as_str());" not in content, f"The bug 'result.push(upper.as_str());' is still present in {TRANSFORMER_RS}."