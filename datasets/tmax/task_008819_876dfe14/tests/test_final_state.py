# test_final_state.py

import os
import subprocess
import pytest

def test_extracted_payloads():
    path = "/home/user/extracted_payloads.txt"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert "ff0a0b" in lines, "Payload 'ff0a0b' is missing from extracted_payloads.txt"
    assert "ff112233" in lines, "Payload 'ff112233' is missing from extracted_payloads.txt"
    assert len(lines) == 2, f"Expected exactly 2 payloads, found {len(lines)}"

def test_regression_test_exists_and_valid():
    path = "/home/user/sysmon/tests/regression.rs"
    assert os.path.isfile(path), f"Regression test file {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert "test_fuzzer_crashes" in content, "Function 'test_fuzzer_crashes' not found in regression.rs"
    assert "sysmon::process_input" in content or "process_input" in content, "Call to process_input not found in regression.rs"

def test_lib_rs_panic_removed():
    path = "/home/user/sysmon/src/lib.rs"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert "panic!" not in content, "panic! macro is still present in src/lib.rs"
    assert "Err(" in content, "Expected an Err return variant in src/lib.rs"

def test_build_rs_fixed():
    path = "/home/user/sysmon/build.rs"
    assert os.path.isfile(path), f"File {path} does not exist"

    with open(path, "r") as f:
        content = f.read()

    assert "cargo:rustc-link-search" in content, "build.rs is missing the cargo:rustc-link-search directive"

def test_cargo_test_passes():
    sysmon_dir = "/home/user/sysmon"
    assert os.path.isdir(sysmon_dir), f"Directory {sysmon_dir} does not exist"

    result = subprocess.run(
        ["cargo", "test"],
        cwd=sysmon_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"cargo test failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"