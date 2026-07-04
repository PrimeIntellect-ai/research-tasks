# test_final_state.py

import os
import pytest

def test_build_patch_exists_and_content():
    patch_path = "/home/user/pipeline/build.patch"
    assert os.path.isfile(patch_path), f"The file {patch_path} is missing. Did you run process.sh?"

    with open(patch_path, "r") as f:
        content = f.read()

    assert "-SIZE=1048576" in content, "build.patch is missing the expected old SIZE line."
    assert "+SIZE=1050000" in content, "build.patch is missing the expected new SIZE line."

def test_build_patch_no_debug_test():
    patch_path = "/home/user/pipeline/build.patch"
    assert os.path.isfile(patch_path), f"The file {patch_path} is missing."

    with open(patch_path, "r") as f:
        content = f.read()

    assert "DEBUG_" not in content, "build.patch contains 'DEBUG_' lines, which should have been filtered out."
    assert "TEST_" not in content, "build.patch contains 'TEST_' lines, which should have been filtered out."

def test_process_sh_no_python():
    script_path = "/home/user/pipeline/process.sh"
    assert os.path.isfile(script_path), f"The file {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "python" not in content.lower(), "process.sh still contains a call to Python. The logic should be translated to Bash."

def test_process_sh_uses_local():
    script_path = "/home/user/pipeline/process.sh"
    assert os.path.isfile(script_path), f"The file {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "local " in content, "process.sh does not use 'local' variables. You need to fix the variable scope bug."

def test_bats_installed():
    bats_bin = "/home/user/local/bin/bats"
    assert os.path.isfile(bats_bin), f"BATS executable not found at {bats_bin}."
    assert os.access(bats_bin, os.X_OK), f"BATS executable at {bats_bin} is not executable."

def test_bats_test_results():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"Test results log not found at {log_path}."

    with open(log_path, "r") as f:
        content = f.read()

    assert "ok" in content.lower(), "The BATS test results do not indicate a successful test run ('ok' not found)."