# test_final_state.py
import os
import subprocess
import hashlib

def test_cargo_test_passes():
    """Verify that the Rust project compiles and tests pass."""
    project_dir = "/home/user/data_api"
    result = subprocess.run(
        ["cargo", "test"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"cargo test failed:\n{result.stderr}\n{result.stdout}"

def test_proptest_implemented():
    """Verify that the proptest_length_invariant is implemented."""
    processor_path = "/home/user/data_api/src/processor.rs"
    assert os.path.isfile(processor_path), f"{processor_path} does not exist"

    with open(processor_path, "r") as f:
        content = f.read()

    assert "proptest_length_invariant" in content, "proptest_length_invariant is not found in processor.rs"
    assert "proptest!" in content, "proptest macro is not used in processor.rs"

def test_musl_binary_exists():
    """Verify that the musl release binary was built successfully."""
    binary_path = "/home/user/data_api/target/x86_64-unknown-linux-musl/release/data_api"
    assert os.path.isfile(binary_path), f"Musl binary not found at {binary_path}"

def test_result_log():
    """Verify that result.log exists and contains the correct information."""
    log_path = "/home/user/result.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist"

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f.read().strip().split('\n')]

    assert len(lines) >= 3, f"result.log should have at least 3 lines, found {len(lines)}"

    assert lines[0] == "TESTS_PASSED", f"Line 1 should be 'TESTS_PASSED', found '{lines[0]}'"
    assert lines[1] == "BUILD_MUSL_PASSED", f"Line 2 should be 'BUILD_MUSL_PASSED', found '{lines[1]}'"

    binary_path = "/home/user/data_api/target/x86_64-unknown-linux-musl/release/data_api"
    if os.path.isfile(binary_path):
        with open(binary_path, "rb") as f:
            expected_hash = hashlib.sha256(f.read()).hexdigest()
        assert lines[2] == expected_hash, f"Line 3 checksum mismatch. Expected {expected_hash}, found {lines[2]}"
    else:
        assert False, "Cannot verify checksum because musl binary is missing"