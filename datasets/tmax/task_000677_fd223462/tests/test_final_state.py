# test_final_state.py

import os
import re

def test_rust_project_exists():
    """Test that the Rust project pow-shield was created."""
    assert os.path.isdir("/home/user/pow-shield"), "The pow-shield directory does not exist."
    assert os.path.isfile("/home/user/pow-shield/Cargo.toml"), "Cargo.toml is missing in pow-shield."
    assert os.path.isfile("/home/user/pow-shield/src/main.rs"), "src/main.rs is missing in pow-shield."

def test_rust_code_requirements():
    """Test that the Rust code uses threads, mpsc, and has tests."""
    main_rs_path = "/home/user/pow-shield/src/main.rs"
    with open(main_rs_path, "r") as f:
        content = f.read()

    assert "std::thread" in content or "thread::" in content, "Code does not seem to use std::thread."
    assert "mpsc" in content, "Code does not seem to use mpsc channels."

    test_count = content.count("#[test]")
    assert test_count >= 2, f"Expected at least 2 unit tests, found {test_count}."

def test_release_binary_exists():
    """Test that the project was built in release mode."""
    binary_path = "/home/user/pow-shield/target/release/pow-shield"
    assert os.path.isfile(binary_path), f"Release binary not found at {binary_path}. Did you run cargo build --release?"

def test_results_log():
    """Test that the results.log contains the correct output."""
    log_path = "/home/user/results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_results = {
        "REQ001: VALID",
        "REQ002: INVALID",
        "REQ003: INVALID",
        "REQ004: INVALID",
        "REQ005: INVALID"
    }

    actual_results = set(lines)
    assert actual_results == expected_results, f"Results in {log_path} do not match expected output."

def test_test_results_log():
    """Test that test_results.log exists and shows successful tests."""
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    assert "test result: ok" in content, "test_results.log does not indicate successful test execution ('test result: ok')."

    # Check that at least 2 tests passed
    passed_match = re.search(r"(\d+) passed", content)
    if passed_match:
        passed_count = int(passed_match.group(1))
        assert passed_count >= 2, f"Expected at least 2 tests to pass, but found {passed_count}."
    else:
        # Fallback if specific cargo test output format varies
        ok_count = content.count("... ok")
        assert ok_count >= 2, "Could not find at least 2 successful tests in test_results.log."