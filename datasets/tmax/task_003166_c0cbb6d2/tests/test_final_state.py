# test_final_state.py

import os
import subprocess
import pytest

def test_block_sh_content():
    script_path = "/home/user/block.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # We look for the required components of the iptables command
    assert "iptables" in content, "The block.sh script does not contain an 'iptables' command."
    assert "-A INPUT" in content or "--append INPUT" in content, "The iptables command must append to the INPUT chain."
    assert "-j DROP" in content or "--jump DROP" in content, "The iptables command must DROP the traffic."
    assert "203.0.113.88" in content, "The iptables command does not block the correct malicious IP (203.0.113.88)."
    assert "8080" in content, "The iptables command does not specify the correct port (8080)."
    assert "-p tcp" in content or "--protocol tcp" in content, "The iptables command does not specify the TCP protocol."

def test_rust_auth_implementation():
    auth_service_dir = "/home/user/auth_service"
    tests_dir = os.path.join(auth_service_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)

    test_file_path = os.path.join(tests_dir, "eval_test.rs")

    # Write a Rust integration test to verify the functionality of the auth module
    test_code = """
use auth_service::auth::{get_safe_redirect, generate_secure_token};

#[test]
fn test_redirect_evil() {
    assert_eq!(get_safe_redirect("http://evil.com"), "https://trusted.corp/home", "Failed to fallback to safe URL for evil.com");
}

#[test]
fn test_redirect_safe() {
    assert_eq!(get_safe_redirect("https://trusted.corp/app"), "https://trusted.corp/app", "Failed to keep trusted URL");
}

#[test]
fn test_token() {
    assert_eq!(
        generate_secure_token("admin"), 
        "2c53b66df87016ea98e72efcc162b70b5550a25fc5f6fb87c672b144fb2b152d",
        "Token generation did not match the expected SHA-256 hash"
    );
}
"""
    with open(test_file_path, "w") as f:
        f.write(test_code)

    # Run the tests using cargo
    result = subprocess.run(
        ["cargo", "test", "--test", "eval_test"],
        cwd=auth_service_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Rust implementation verification failed. "
        f"Cargo test output:\n{result.stdout}\n{result.stderr}"
    )