# test_final_state.py

import os
import re

def test_build_rs_fixed():
    path = "/home/user/sec-payload-verifier/build.rs"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "cc::Build::new()" in content or "cc::Build" in content, "build.rs does not appear to use the cc crate to build the C file."
    assert "src/fast_chk.c" in content, "build.rs does not reference 'src/fast_chk.c'."
    assert "compile" in content, "build.rs does not call compile()."

def test_github_actions_workflow():
    path = "/home/user/sec-payload-verifier/.github/workflows/ci.yml"
    assert os.path.isfile(path), f"GitHub Actions workflow file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "cargo test" in content, "Workflow file does not contain 'cargo test'."
    assert "ubuntu-latest" in content, "Workflow file does not contain 'ubuntu-latest'."
    assert "push" in content, "Workflow file does not trigger on 'push'."

def test_results_log():
    path = "/home/user/test_results.log"
    assert os.path.isfile(path), f"Test results log file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "test result: ok" in content.lower(), "Test results log does not indicate a successful test run ('test result: ok')."
    assert "test_ffi_checksum_matches_rust" in content, "Test results log does not show the property test being run."