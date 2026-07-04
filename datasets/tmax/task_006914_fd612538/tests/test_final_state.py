# test_final_state.py

import os
import pytest

def test_test_results_log_exists():
    path = "/home/user/test_results.log"
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the cargo test command and redirect the output?"

def test_test_results_log_contents():
    path = "/home/user/test_results.log"
    with open(path, "r") as f:
        content = f.read()

    assert "test tests::test_mul_properties ... ok" in content, "The property test `test_mul_properties` did not run successfully or was not found in the log."

def test_build_rs_logic():
    path = "/home/user/rust-linker-debug/build.rs"
    with open(path, "r") as f:
        content = f.read()

    assert "serde_json" in content, "build.rs does not appear to use serde_json to parse the manifest."
    assert "semver" in content or "Version" in content, "build.rs does not appear to use semver for version checking."
    assert "cargo:rustc-cfg=use_v2" in content, "build.rs does not output the 'cargo:rustc-cfg=use_v2' flag."

def test_lib_rs_logic():
    path = "/home/user/rust-linker-debug/src/lib.rs"
    with open(path, "r") as f:
        content = f.read()

    assert "use_v2" in content, "src/lib.rs does not appear to use the 'use_v2' cfg flag."
    assert "proptest" in content, "src/lib.rs does not appear to use the proptest macro/crate."
    assert "ops_mul_v2" in content, "src/lib.rs does not declare or call ops_mul_v2."