# test_final_state.py

import os
import subprocess
import pytest

def test_resolution_txt_correct():
    path = "/home/user/resolution.txt"
    assert os.path.isfile(path), f"Resolution file {path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert len(lines) >= 2, f"Expected at least 2 lines in {path}, found {len(lines)}"
    assert lines[0] == "TRACE_ID: TXN-7734-ALPHA-09", f"Line 1 incorrect. Got: {lines[0]}"
    assert lines[1] == "FIXED_TEST_COST: 0", f"Line 2 incorrect. Got: {lines[1]}"

def test_rust_code_behavior():
    project_dir = "/home/user/billing-service"
    main_path = os.path.join(project_dir, "src", "main.rs")
    log_path = "/home/user/trace_output.log"

    # Remove existing log to ensure we capture the current function's output
    if os.path.exists(log_path):
        os.remove(log_path)

    # Create a simple main.rs to test the library function
    test_code = """
fn main() {
    let cost = billing_service::calculator::calculate_cost(1500, 3, 5000);
    println!("{}", cost);
}
"""
    with open(main_path, "w") as f:
        f.write(test_code)

    # Run the test code
    result = subprocess.run(
        ["cargo", "run", "--quiet"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Cargo build/run failed:\n{result.stderr}"

    output = result.stdout.strip()
    assert output == "0", f"Expected calculated cost to be 0, but got: {output}"

    # Verify the log was created and contains the correct trace
    assert os.path.isfile(log_path), f"Log file {log_path} was not created by the function."

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_log = "[TXN-7734-ALPHA-09] Intermediate Subtotal: 4500"
    assert expected_log in log_content, f"Expected log entry '{expected_log}' not found in {log_path}. Content:\n{log_content}"

    # Clean up main.rs
    os.remove(main_path)